import argparse
import numpy as np
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def cv_stat(index, preds_dir, output_dir, folds=['v1', 'v2', 'v3', 'v4', 'v5']):
    """
    Compute the mean and standard deviation of cross validation models, and write the result to 
        a parquet file.

    Parameters
    ----------
    index (int): The index of the two files that are going to be concatenated.
    preds_dir (str): Path to the predictions of the models. 
    output_dir (str): Output directory. 
    folds (List[str]): The list of prediction folds to concatenate.

    Returns
    -------
    None
    """
    df = pd.DataFrame()
    first_df = True

    for fold in folds:
        file = preds_dir + '/' + fold + '/file{}.parquet'.format(index)
        preds = pd.read_parquet(file)

        if first_df:
            df = preds
            df.rename(columns={'preds':fold}, inplace=True)
            first_df = False
        else:
            df[fold] = preds['preds']
    
    df['mean'] = df[folds].mean(axis=1)
    df['std'] = df[folds].std(axis=1)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df.to_parquet(output_dir + '/file{}'.format(index) + '.parquet')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--index", type=int)
    parser.add_argument("--preds_dir")
    parser.add_argument("--output_dir")
    parser.add_argument("--folds", nargs='+', type=str)

    args = parser.parse_args()

    cv_stat(args.index, args.preds_dir, args.output_dir, args.folds)

if __name__ == "__main__":
    main()