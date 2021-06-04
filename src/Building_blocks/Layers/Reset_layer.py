
################################################################################################################
"""
Placeholder layer used to signal to model to reset run parameters to default
"""

# Built-in/Generic Imports

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class RESET_layer(Layer):
    def __init__(self, evaluation_function_bool: bool, step_bool: bool, max_step_bool: bool):
        super().__init__()

        self.layer_ref = "      "
        self.layer_type = "RESET_layer"

        self.evaluation_function_bool = evaluation_function_bool
        self.step_bool = step_bool
        self.max_step_bool = max_step_bool

        return

    def __str__(self):
        return f"> {self.layer_type}"

    def step(self, population=None, evaluation_function=None, epoch=None, max_epoch=None):
        return self.evaluation_function_bool, self.step_bool, self.max_step_bool
