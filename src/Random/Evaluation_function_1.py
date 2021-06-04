
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


def param_sum(individual):
    total = 0

    for parameter in individual.parameter_set.values():
        total += parameter

    return total
