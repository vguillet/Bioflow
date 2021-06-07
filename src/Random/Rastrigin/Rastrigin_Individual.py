
################################################################################################################
"""
Placeholder layer used to signal to model to reset run parameters to default
"""

# Built-in/Generic Imports
import random

# Libs
from faker import Faker

# Own modules
from src.Building_blocks.abc_Individual import Individual


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Rastrigin_Indvidual(Individual):
    def __init__(self):
        super().__init__()

        self.nb_of_adjustable_parameters = 2
        self.parameter_set = {"x": -5.12 + (5.12 - -5.12) * random.random(),
                              "y": -5.12 + (5.12 - -5.12) * random.random(),
                              "test": {"v": 1,
                                       "w": 0}}

        # self.name = Faker().name()

        return

    def gen_parameter_set(self):
        return
