import argparse

import numpy as np

import deepchem as dc
from deepchem.models import WandbLogger
from deepchem.models import ValidationCallback

from src.model_creator import ModelCreator
from src.scheduler_creator import SchedulerCreator
from src.utils.optimizers import AdamW
from src.utils.score_function import spearmanr
from utils.utils import load_data, yaml_parser


def train(config: dict) -> None:
    """
    Train the model.

    Parameters
    ----------
    config (dict): Training configurations. Please refer to example yaml files for more details.

    Returns
    -------
    None
    """
    logger = WandbLogger(project=config['wandb']['project'], 
                         group=config['wandb']['group'],
                         config=config)

    train_dataset = load_data(config['data']['training'])
    valid_dataset = load_data(config['data']['validation'])

    train_dataset = train_dataset.complete_shuffle()
    valid_dataset = valid_dataset.complete_shuffle()

    if config['data']['normalize']:
        train_transformer = dc.trans.NormalizationTransformer(transform_y=True, dataset=train_dataset)
        train_dataset = train_transformer.transform(train_dataset)
        valid_dataset = train_transformer.transform(valid_dataset)

    metrics = [dc.metrics.Metric(spearmanr, mode="regression"),
               dc.metrics.Metric(dc.metrics.pearson_r2_score), 
               dc.metrics.Metric(dc.metrics.mean_squared_error)]
    
    vc_valid = ValidationCallback(valid_dataset, 
                                  interval=100, 
                                  metrics=metrics, 
                                  save_dir=config['model']['best_ckpt'],
                                  save_on_minimum=False,
                                  transformers=[])

    learning_rate = SchedulerCreator(config['optimization']).get_scheduler()
    optimizer = AdamW(learning_rate=learning_rate, weight_decay=0.0001)

    model = ModelCreator(config['model'],
                   optimizer=optimizer,
                   wandb_logger=logger).get_model()

    n_epoch = config['optimization']['n_epoch']

    counter = 0
    patience = config['optimization']['early_stopping']['patience']
    smoothing_factor = config['optimization']['early_stopping']['smoothing_factor']
    initial_training = config['optimization']['early_stopping']['initial_training']

    for i in range(n_epoch):
                
        if counter > patience:
            break
        
        model.fit(train_dataset, 
                  nb_epoch=1, 
                  restore=config['model']['restore'],
                  max_checkpoints_to_keep=1, 
                  callbacks=[vc_valid])

        val_result = model.evaluate(valid_dataset, 
                                    metrics=metrics, 
                                    transformers=[])

        r = val_result['spearmanr']

        if i == 0:
            prev_ema_r = r
        
        ema_r = r * (1 - smoothing_factor) + prev_ema_r * smoothing_factor
        
        if (round(prev_ema_r, 4) >= round(ema_r, 4)) and i > initial_training:
            counter += 1
        else:
            counter = 0

        prev_ema_r = ema_r


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    
    args = parser.parse_args()

    config = yaml_parser(args.config)

    train(config)

if __name__ == "__main__":
    main()
