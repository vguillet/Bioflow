
################################################################################################################
"""
Placeholder layer used to signal to model to reset run parameters to default
"""

# Built-in/Generic Imports
import random

# Own modules
from src.Building_blocks.abc_Individual import Individual

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Indvidual_1(Individual):
    def __init__(self, parameter_set=None):
        super().__init__()

        self.parameter_set = {"a": random.randint(0, 100),
                              "b": random.randint(0, 100),
                              "c": random.randint(0, 100),
                              "d": random.randint(0, 100)}

        return

    def gen_parameter_set(self):
        return
