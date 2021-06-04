
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


class Randomiser_1:
    @staticmethod
    def modify_param(offspring,
                     parameter_to_modify,
                     current_generation,
                     nb_of_generations,
                     parameters_decay_function):

        offspring.parameter_set[parameter_to_modify] += random.randint(0, 10)

        return offspring
