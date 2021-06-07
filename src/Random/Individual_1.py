
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


class Indvidual_1(Individual):
    def __init__(self):
        super().__init__()

        self.fitness_history = []
        self.nb_of_adjustable_parameters = 4

        self.parameter_set = {"a": random.randint(-100, 100),
                              "b": random.randint(-100, 100),
                              "c": random.randint(-100, 100),
                              "d": random.randint(-100, 100)}

        # self.name = Faker().name()

        return

    def gen_parameter_set(self):
        return
