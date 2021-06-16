
################################################################################################################
"""
Placeholder layer used to signal to model to reset run parameters to default
"""

# Built-in/Generic Imports
import random
from copy import deepcopy

# Libs
from flatten_dict import flatten

# Own modules
from src.Building_blocks.Parameter_tools import get_from_dict, add_in_dict
from src.Building_blocks.abc_Individual import Individual

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Rastrigin_randomiser:
    @staticmethod
    def modify_param(parameter_set,
                     parameter_to_modify,
                     current_generation,
                     nb_of_generations,
                     parameters_decay_function):

        if parameter_to_modify == "x" or parameter_to_modify == "y":
            add_in_dict(parameter_set, list(parameter_to_modify), random.randint(-1, 1))
        else:
            pass

        return parameter_set
