
################################################################################################################
"""
STEP layer base class, to be used as parent to build STEP layers
"""

# Built-in/Generic Imports
import json
import random

# Libs

# Own modules
import src.Random.Parameter_randomiser_1
from src.Building_blocks.Layers.abc_Layer import Layer
from src.Tools.Parameter_tools import select_parameter_to_modify
from src.Building_blocks.Population import Population


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class STEP_layer(Layer):
    def __init__(self, verbose=0):
        super().__init__()

        self.layer_ref = None
        self.layer_type = "STEP_layer"

        self.verbose = verbose

        return

    def __str__(self):
        return f"> {self.layer_type}"

    def step(self, population, evaluation_function, epoch, max_epoch):
        return population
