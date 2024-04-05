import numpy as np


def upgrade_mw_tier(max_up_attempts=15):
    """
    Simulates process of masterworking in D4.
    
    Args:
        max_up_attempts (int): The maximum number of upgrade attempts allowed.
    
    Returns:
        int: The final masterwork level achieved.
    """    
    MAX_UP_ATTEMPTS = max_up_attempts
    # current masterwork level upgrade probability
    # tier 1-4 is 100% success rate so we start at level 5 which is index 4
    # our initial level is 4, so we use level to index the upgrade_probs list
    upgrade_probs = [1, 1, 1, 1, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2]
    MAX_LEVEL = 12
    level = 4
    for _ in range(MAX_UP_ATTEMPTS):
        # condition reduces the number of iterations per worker without affecting the result
        if level == MAX_LEVEL:
            break
        
        event = np.random.choice([False, True], p=[1-upgrade_probs[level], upgrade_probs[level]])
        if event:
            level += 1
        else:
            # bad luck protection, if we fail, add 10% to the success rate
            upgrade_probs[level] += 0.1

    return level


class Sim:
    """
    class wrapper for simulation functions.
    2 methods are defined to handle simulations with and without keyword arguments.
    """

    def __init__(self, target_sim):
        self.target_sim = target_sim

    def run_simulation(self, n):
        # run n times per worker. 1 cpu core = 1 worker
        return sum(self.target_sim() for _ in range(n))

    def run_with_kargs(self, args):
        # run n times per worker. 1 cpu core = 1 worker
        n, kargs = args
        return [self.target_sim(**kargs) for _ in range(n)]


def pooled_simulation(sim, n, **kargs):
    """helper function to prepare and run simulations in parallel using multiprocessing.Pool."""
    from multiprocessing import Pool, cpu_count
    s = Sim(sim)
    # start = time.time()
    num_processors = cpu_count()
    pool = Pool(processes=num_processors)
    trials_per_worker = n // num_processors
    if kargs:
        results = pool.map(s.run_with_kargs, 
                           [(trials_per_worker, dict(**kargs))]*num_processors)
        # we can check the p of other tiers by changing the integer in the line below
        total = np.sum(np.array(results) == 12)/n
        outstr = f'Probability of reaching tier 12 using permutations: {n} \n'
        # simple formatting for output
        # outstr += f'    iterations per worker (n_cpu: {num_processors}): {trials_per_worker}\n'
        outstr += f'    max attempts per iteration: {kargs["max_up_attempts"]}\n'
        outstr += f'    p = {total}\n'
        
    else:
        # no kargs, default to simple simulation whose return value is 1 or 0, success or failure,
        # not an array representing multilevel outcomes like the upgrade_mw_tier function
        results = pool.map(s.run_simulation, 
                           [trials_per_worker]*num_processors)
        total = sum(results)/n
        outstr = f'Probability of event happening: {total} \n'
        outstr += f'trials per worker (n_cpu: {num_processors}): {trials_per_worker}'

    print(outstr)
    # e_time = time.time() - start
    # print(f'Run Time: {e_time : .6f} seconds')


if __name__ == "__main__":
    # import time
    import argparse
    parser = argparse.ArgumentParser(description='Run Monte Carlo Simulations')
    #
    # new simulations can be added to the choices list, I use function.__name__ syntax.
    # It allows vscode to autocomplete & refactor function name changes.
    parser.add_argument('sim',
                        type=str,
                        help='example usage cmd: python mw_rollout.py upgrade_mw_tier',
                        choices=[upgrade_mw_tier.__name__])
    args = parser.parse_args()
    # example usage cmd: python mw_rollout.py upgrade_mw_tier
    if args.sim == upgrade_mw_tier.__name__:
        print(f'running simulations')
        pooled_simulation(upgrade_mw_tier, 100000, max_up_attempts=25)
            
    #
    # add more simulations here, such as a new version of the current masterwork tier upgrade simulation.
    # elif args.sim == upgrade_mw_tier_with_protection.__name__:
    #     pooled_simulation(upgrade_mw_tier_with_protection, 100000, max_up_attempts=30)

    else:
        print(f'Invalid Simulation Name: {args.sim}')
        exit()
