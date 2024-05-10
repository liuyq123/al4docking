from utils.optimizers import LinearLR, CosineAnnealingLR, SequentialLR, CyclicLR, ExponentialDecay

class SchedulerCreator:
    """
    Initializes a scheduler.
    """

    def __init__(self, optimization_config):

        self.config = optimization_config

    def get_scheduler(self):

        schedulers = {
            "cosine": CosineAnnealingLR,
            "cyclic": CyclicLR,
            "exponential": ExponentialDecay,
            "linear": LinearLR
        }
        
        scheduler_name = self.config['scheduler']
        warmup_steps = self.config['warmup_steps']

        if warmup_steps != 0:
            scheduler1 = LinearLR(self.config['learning_rate'], 0.0, 1.0, warmup_steps)
            scheduler2 = schedulers[scheduler_name](self.config['learning_rate'], **self.config['scheduler_params'])
            
            scheduler = SequentialLR(self.config['learning_rate'], [scheduler1, scheduler2], [self.config['warmup_steps']])
        else:
            scheduler = schedulers[scheduler_name](self.config['learning_rate'], **self.config['scheduler_params'])

        return scheduler