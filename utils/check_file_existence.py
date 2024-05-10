import argparse
import numpy as np
import pandas as pd
import os

def load_predictions(preds_data_path: str, 
                     total_file_num: int) -> None:
    """
    Print the index of the files that don't exist.

    Parameters
    ----------
    preds_data_path (str): Path to the prediction directory.
    total_file_num (int): Total number of files supposed to be there. 

    Returns
    -------
    None
    """
    for i in range(total_file_num):

        file = preds_data_path  + '/file{}'.format(i+1)+ '.parquet'

        if os.path.exists(file) == False:
            print(i+1, end=',')
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--preds_data_path")
    parser.add_argument("--total_file_num", type=int)

    args = parser.parse_args()

    load_predictions(args.preds_data_path, args.total_file_num)
