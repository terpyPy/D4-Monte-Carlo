# pkldf unit tests
import os
import numpy as np
import unittest
import re
import pkldf as pydf


class TestPklDF(unittest.TestCase):
    def test_dict(self):
        successful_asserts = 0

        pkl_test_dict = pydf.PklManager('', pattern='dict_*.pkl')

        self.assertEqual(pkl_test_dict.files, ['dict_r.pkl'])
        successful_asserts += 1

        pkl_test_dict.load_all()
        EXPECTED_NAMES = [f'results_{i}' for i in range(1,30)]

        col_names = list(pkl_test_dict.results.keys())
        self.assertEqual(col_names, EXPECTED_NAMES)
        successful_asserts += 1

        df = pkl_test_dict.as_df()

        self.assertEqual(df.shape, (100000, 29))
        successful_asserts += 1

        self.assertEqual(list(df.columns), EXPECTED_NAMES)
        successful_asserts += 1

        print(f'test_dict: OK, {successful_asserts} assertions passed')
        
    def test_list(self):
        successful_asserts = 0
        pkl_test_dir = pydf.PklManager('run_2', pattern='results_*.pkl')
        # apply a sort to the files list
        pkl_test_dir.sort(k=lambda x: int(re.search('results_(\d+)', x).group(1)))
        # expected file names
        EXPECTED_F_NAMES = [f'results_{i}.pkl' for i in range(1,30)]
        # get base names for easier comparison/sanitization
        col_f_names = [os.path.basename(f) for f in pkl_test_dir.files]
        # assert the sorted file names are as expected
        self.assertEqual(col_f_names, EXPECTED_F_NAMES)
        successful_asserts += 1
        # load the files
        pkl_test_dir.load_all()
        # make a version of the expected names that are sanitized for column names
        EXPECTED_NAMES = [s.split('.')[0] for s in EXPECTED_F_NAMES]
        # get the column names
        col_names = list(pkl_test_dir.results.keys())
        # assert the column names are as expected
        self.assertEqual(col_names, EXPECTED_NAMES)
        successful_asserts += 1
        # get the data frame
        df = pkl_test_dir.as_df()
        # assert the shape of the data frame is as expected
        self.assertEqual(df.shape, (100000, 29))
        successful_asserts += 1
        # assert the column names of the data frame are as expected
        self.assertEqual(list(df.columns), EXPECTED_NAMES)
        successful_asserts += 1
        print(f'test_list: OK, {successful_asserts} assertions passed')
        
    def test_2d_list(self):
        successful_asserts = 0
        pkl_test_dir = pydf.PklManager('', pattern='2d_list.pkl')
        # expected file names
        EXPECTED_F_NAMES = ['2d_list.pkl']
        self.assertEqual(pkl_test_dir.files, EXPECTED_F_NAMES)
        successful_asserts += 1
        pkl_test_dir.load_all()
        EXPECTED_RESULTS = [list(range(3)) for _ in range(3)]
        self.assertEqual(pkl_test_dir.results, EXPECTED_RESULTS)
        successful_asserts += 1
        df = pkl_test_dir.as_df()
        self.assertEqual(df.shape, (3, 3))
        successful_asserts += 1
        self.assertEqual(list(df.columns), [0, 1, 2])
        successful_asserts += 1
        print(f'test_2d_list: OK, {successful_asserts} assertions passed')
        
    def test_2d_list_dset(self):
        pkl_dir = pydf.PklManager('test_files', pattern='2d_set.pkl')
        pkl_dir.load_all()
        df = pkl_dir.as_df(transpose=True)
        self.assertEqual(df.shape, (100000, 29))
        self.assertEqual(list(df.columns), [i for i in range(29)])
        # val should be > 0 and < 0.1
        val = df.apply(lambda x: np.mean(x == 12))[7]
        self.assertTrue(val > 0.0)
        self.assertTrue(val < 0.1)
        print('test_2d_list_dset: OK')
        