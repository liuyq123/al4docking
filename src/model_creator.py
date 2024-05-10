import deepchem as dc
from deepchem.models import GCNModel, GATModel
from deepchem.models.wandblogger import WandbLogger

import torch.nn.functional as F

from typing import Optional

from utils.optimizers import Optimizer

class ModelCreator:
    """
    Initializes a model.
    """

    def __init__(self, 
                 model_config: dict, 
                 optimizer: Optional[Optimizer] = None,
                 wandb_logger: Optional[WandbLogger] = None) -> None:

        self.config = model_config
        self.optimizer = optimizer
        self.wandb_logger = wandb_logger

    def get_model(self):

        if 'activation' in self.config['params']:
            self.config['params']['activation'] = eval(self.config['params']['activation'])

        models = {
            "gcn": GCNModel,
            "gat": GATModel
        }
        
        model_name = self.config['name']

        return models[model_name](**self.config['params'], 
                                  n_tasks=1,
                                  optimizer=self.optimizer,
                                  wandb_logger=self.wandb_logger)
