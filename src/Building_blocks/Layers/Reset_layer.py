
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
    def __init__(self,
                 evaluation_function_bool: bool,
                 step_bool: bool,
                 max_step_bool: bool,
                 verbose=0):
        super().__init__()

        self.layer_ref = "      "
        self.layer_type = "RESET_layer"

        self.evaluation_function_bool = evaluation_function_bool
        self.step_bool = step_bool
        self.max_step_bool = max_step_bool

        self.verbose = verbose

        return

    def __str__(self):
        return f"> {self.layer_type}"

    def step(self, population=None, evaluation_function=None, epoch=None, max_epoch=None):
        if self.verbose == 1:
            print(f"---- << RESET layer >> ----")
            print(f" Reset evaluation function: {self.evaluation_function_bool}")
            print(f" Reset step: {self.step_bool}")
            print(f" Reset max step: {self.max_step_bool}")
            print("\n")

        return self.evaluation_function_bool, self.step_bool, self.max_step_bool
