
################################################################################################################
"""
STEP layer base class, to be used as parent to build STEP layers
"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class STEP_layer(Layer):
    def __init__(self,
                 verbose=0,
                 name=""):

        # --> Meta
        self.ref = "      "
        self.type = "STEP"
        self.name = name

        self.verbose = verbose

        return

    def __str__(self):
        return f"  -> {self.name} ({self.type})"

    def step(self, population, evaluation_function, epoch, max_epoch, data=None):
        return population
