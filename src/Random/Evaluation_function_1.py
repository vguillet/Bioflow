
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


def param_sum(individual):
    total = - (individual.parameter_set["a"]
               - individual.parameter_set["b"]
               - 10 * individual.parameter_set["c"]
               + 0 * individual.parameter_set["d"])**2

    return total
