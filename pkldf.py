import os
import glob
import pandas as pd
import ftools as ft



class PklManager(list):
    def __init__(self, directory, pattern='*_*.pkl'):
        """
        Initialize the PklDF object. 
        This is an intermediate representation of the pickle files in a dir that can be converted to a DataFrame.
        

        Args:
            directory (str): The directory path where the pickle files are located.
            pattern (str, optional): The file pattern to match the pickle files. Defaults to '*_*.pkl'.
        """
        self.directory = directory
        self.files = glob.glob(os.path.join(directory, pattern))
        self.results = {}
        
        
    def load_all(self):
        """inplace, load all the pickle files we found in the directory."""
        if len(self.files) == 1:
            self.results = ft.load_plk_results(self.files[0], self.directory)
        
        else:    
            
            for file in self.files:
                colmn_name = file.split('\\')[-1].split('.')[0]
                self.results[colmn_name] = ft.load_plk_results(file, self.directory)
            
    def get_results(self):
        return self.results

    def get_files(self):
        return self.files

    def get_directory(self):
        return self.directory
    
    def sort(self, k=None):
        '''sort in place on files list. k is a function that takes a filename and returns a key to sort on.'''
        self.files.sort(key=k)

    def as_df(self, transpose=False):
        """Convert the results to a DataFrame. load_all() must be called first, otherwise it will return an empty DataFrame."""
        if transpose:
            return pd.DataFrame(self.results).T
        return pd.DataFrame(self.results)
    