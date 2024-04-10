# ftools
# A collection of file utilities
import os
import pickle


def save_results(results, filename, directory=''):
    # Ensure filename is just a filename, not a path
    filename = os.path.basename(filename)
    if directory != '':
        directory = directory + "\\"
    # Construct the full path safely
    full_path = os.path.join(os.getcwd(), directory+filename)

    with open(full_path, 'wb') as f:
        pickle.dump(results, f)
    print(f'results array saved to {filename}')
    
def load_plk_results(filename, directory=''):
    # Ensure filename is just a filename, not a path
    filename = os.path.basename(filename)
    if directory == '':
        
        # Construct the full path safely
        full_path = os.path.join(os.getcwd(), filename)
        
    else:
        full_path = os.path.join(os.getcwd(), directory+"\\"+filename)

    with open(full_path, 'rb') as f:
        results = pickle.load(f)
        
    return results
