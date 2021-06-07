
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import numpy as np

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


def Rastrigin_function(individual, data=None, settings=None):
    return (individual.parameter_set["x"] ** 2 - 10 * np.cos(2 * np.pi * individual.parameter_set["x"])) + \
           (individual.parameter_set["y"] ** 2 - 10 * np.cos(2 * np.pi * individual.parameter_set["y"])) + 20

