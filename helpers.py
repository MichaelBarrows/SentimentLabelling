import pandas as pd
import numpy as np
import operator
import dataset
import csv
import os

# load_dataset()
# parameters:
#   imput_csv : string - CSV filename and path
# returns:
#   df : DataFrame - dataframe containing the data from the CSV file
# description:
#   This function imports a CSV file as a Pandas DataFrame and returns the
#       DataFrame.
def load_dataset(input_csv):
    df = pd.read_csv(input_csv, header=0, low_memory=False)
    return df

# dataframe_to_csv()
# parameters:
#   pd_df : DataFrame - dataframe to be stored
#   filename : string - path and filename for storage file
# returns:
#   None
# description:
#   This function outputs the dataframe to a CSV file.
def dataframe_to_csv(pd_df, filename):
    pd_df.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)
    return

# data_to_file_two_values()
# parameters:
#   data : list - nested list of data to be stored
#   headings : string - string with heading values
#   filename : string - path and filename to store in
# returns:
#   None
# description:
#   This function stores data in a file (where the data has two values for
#       each row).
def data_to_file_two_values(data, headings, filename):
    with open(filename, mode='w') as file_writer:
        file_writer.write(headings + "\n")
        for row in data:
            file_writer.write(str(row[0]) + ',"' + str(row[1]) + '"' + "\n")
    return

# path_checker()
# parameters:
#   path : string - path to check
# returns:
#   None
# description:
#   This function checks if a given path exists. If the path does not exist, it
#       is created (in a loop, so that each part is created in turn).
def path_checker(path):
    path = path.split("/")
    path_so_far = ""
    for dir in path:
        path_so_far += "/" + dir
        if os.path.exists(path_so_far) == False:
            path_creator(path_so_far)
    return

# path_creator()
# parameters:
#   path : string - the path to be created
# returns:
#   None
# description:
#   This function creates a given path.
def path_creator(path):
    os.mkdir(path)
    return

# path_fetcher()
# parameters:
#   path : string - the path to be looked in
# returns:
#   : list - list of the directory's contents.
# description:
#   This function returns a list of files and folders contained in a directory.
def path_fetcher(path):
    return os.listdir(path)

def sort_dict(dictionary):
    return dict(sorted(dictionary.items(),	
                    key=operator.itemgetter(1),
                    reverse=True))
