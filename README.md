# Monte Carlo Simulations for Masterwork Tier Upgrades

This script simulates the process of upgrading masterwork tiers in D4 using Monte Carlo simulations. It includes a function for running the simulation, a helper function for running the simulations in parallel using multiprocessing, and a main function that parses command line arguments and runs the appropriate simulation.

## Functions

- `upgrade_mw_tier(max_up_attempts=15)`: Simulates the process of upgrading masterwork tiers in D4. Returns the final masterwork level achieved.

- `Sim`: A class that wraps the simulation functions. It has two methods for running simulations with and without keyword arguments.

- `save_results(results, filename)`: Saves the results of a simulation to a file.

- `pooled_simulation(sim, n, **kargs)`: A helper function that prepares and runs simulations in parallel using multiprocessing.

## Usage

To run the script, use the following command:

```bash
python mw_rollout.py <simulation_name>
```

where <simulation_name> is the name of the simulation you want to runs the name of the simulation you want to run. The available simulations are `upgrade_mw_tier` and `run_mw_batch`.

For example, to run the upgrade_mw_tier simulation, use the following command:

```bash
python mw_rollout.py upgrade_mw_tier
```

## Output
The script prints the probability of reaching tier 12 and the total run time. It also saves the results of the simulation as pickle files in form `results_<num_max_attempts>.pkl`.

## Requirements
- Python 3.9+
- numpy
- multiprocessing
for notebook:
- matplotlib
- re
- pandas
