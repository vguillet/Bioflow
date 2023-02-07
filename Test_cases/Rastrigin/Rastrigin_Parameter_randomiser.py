
################################################################################################################
"""
Placeholder layer used to signal to model to reset run parameters to default
"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Tools.Parameter_tools import *

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


def Rastrigin_randomiser(parameter_set,
                         parameter_to_modify: tuple,
                         current_epoch: int,
                         parameters_throttle_curves: dict = None):

    if parameter_to_modify == "x" or parameter_to_modify == "y":
        add_in_dict(parameter_set, list(parameter_to_modify), random.randint(-1, 1))
    else:
        pass

    return parameter_set
