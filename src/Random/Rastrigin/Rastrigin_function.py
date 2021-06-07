
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


def Rastrigin_function(individual):
    return (individual.parameter_set["x"] ** 2 - 10 * np.cos(2 * np.pi * individual.parameter_set["x"])) + \
           (individual.parameter_set["y"] ** 2 - 10 * np.cos(2 * np.pi * individual.parameter_set["y"])) + 20

