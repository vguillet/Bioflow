
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import random

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2021'

##################################################################################################################


def select_parameter_to_modify(parameter_set, parameter_blacklist):
    # --> Select parameter class to modify
    parameter_to_modify = random.choice(list(parameter_set.keys()))

    while parameter_to_modify in parameter_blacklist:
        parameter_to_modify = random.choice(list(parameter_set.keys()))

    # --> Select parameter type to modify
    if type(parameter_to_modify) is dict:
        return select_parameter_to_modify(parameter_to_modify, parameter_blacklist)

    else:
        return parameter_to_modify
