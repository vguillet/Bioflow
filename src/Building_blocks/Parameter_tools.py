
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from functools import reduce  # forward compatibility for Python 3
import operator

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2021'

##################################################################################################################


def select_random_parameter_to_modify(parameter_set, parameter_blacklist):
    # --> Select parameter class to modify
    parameter_to_modify = random.choice(list(parameter_set.keys()))

    while parameter_to_modify in parameter_blacklist:
        parameter_to_modify = random.choice(list(parameter_set.keys()))

    # --> Select parameter type to modify
    if isinstance(parameter_set[parameter_to_modify], dict):
        return select_random_parameter_to_modify(parameter_set[parameter_to_modify], parameter_blacklist)

    else:
        return parameter_to_modify


def get_from_dict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def set_in_dict(dataDict, mapList, value):
    get_from_dict(dataDict, mapList[:-1])[mapList[-1]] = value


def add_in_dict(dataDict, mapList, value):
    get_from_dict(dataDict, mapList[:-1])[mapList[-1]] += value
