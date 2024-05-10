import argparse
import os

import numpy as np
import pandas as pd

from deepchem.data import DiskDataset

from src.utils.utils import yaml_parser
from src.model_creator import ModelCreator

def predict(config: dict, 
            featurized_data_path: str, 
            raw_data_path: str,
            id_field: str,
            output_dir: str,
            output_name: str) -> None:
    """
    Make predictions with the trained model.

    Parameters
    ----------
    config (dict): A dictionary contains the parameters need to restore the model. 
        Can be loaded from the same yaml file used for training.
    featurized_data_path (str): Path to the featurized data.
    raw_data_path (str): Path to the corresponding csv file.
    id_field (str): The name of the id column.
    output_dir (str): The output directory for the predictions. 
    output_name (str): The name of the output file.

    Returns
    -------
    None
    """

    model = ModelCreator(config['model']).get_model()
    model.restore(model_dir=config['model']['best_ckpt'])

    dataset = DiskDataset(featurized_data_path)

    predictions = model.predict(dataset)

    df = pd.read_csv(raw_data_path)
    df['preds'] = predictions
    output = df[[id_field, 'preds', 'smiles']]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output.to_parquet(output_dir + '/' + output_name + '.parquet', index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--featurized_data_path")
    parser.add_argument("--raw_data_path")
    parser.add_argument("--id_field")
    parser.add_argument("--output_dir")
    parser.add_argument("--output_name")
    
    args = parser.parse_args()

    config = yaml_parser(args.config)

    predict(config, args.featurized_data_path, args.raw_data_path, args.id_field, args.output_dir, args.output_name)

if __name__ == "__main__":
    main()