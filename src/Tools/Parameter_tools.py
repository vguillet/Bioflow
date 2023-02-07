
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from functools import reduce  # forward compatibility for Python 3
import operator
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2021'

##################################################################################################################


def select_random_parameter_to_modify(individual, layer_parameter_blacklist: list):
    parameter_set = individual.parameter_set

    # -> Merge individual parameter blacklist with layer parameter blacklist
    parameter_blacklist = (individual.parameter_blacklist + layer_parameter_blacklist)

    # -> Get parameter key map
    key_map = list(flatten_dict(dataDict=deepcopy(parameter_set)).keys())

    # -> Select parameter class to modify
    parameter_to_modify = random.choice(key_map)

    while any(item in parameter_to_modify for item in parameter_blacklist) is True:
        parameter_to_modify = random.choice(key_map)

    return parameter_to_modify

    # # -> Select parameter type to modify
    # if isinstance(get_from_dict(dataDict=parameter_set, mapList=parameter_to_modify), dict):
    #     return select_random_parameter_to_modify(individual=get_from_dict(dataDict=parameter_set,
    #                                                                       mapList=parameter_to_modify),
    #                                              layer_parameter_blacklist=parameter_blacklist)
    #
    # else:
    #     return parameter_to_modify


def get_from_dict(dataDict: dict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def set_in_dict(dataDict: dict, mapList, value):
    get_from_dict(dataDict, mapList[:-1])[mapList[-1]] = value


def add_in_dict(dataDict: dict, mapList, value):
    get_from_dict(dataDict, mapList[:-1])[mapList[-1]] += value


def flatten_dict(dataDict: dict, parent_key=None):
    """
    Flatten a dictionary to return a dict with only one level of keys (tuples)

    :param dataDict:
    :return:
    """

    items = {}

    for key, value in dataDict.items():
        if isinstance(value, dict):
            if parent_key is not None:
                items.update(flatten_dict(dataDict=value, parent_key=(parent_key, key)).items())
            else:
                items.update(flatten_dict(dataDict=value, parent_key=(key)).items())
        else:
            if parent_key is not None:
                if isinstance(parent_key, tuple):
                    items[(*parent_key, key)] = value
                else:
                    items[(parent_key, key)] = value
            else:
                items[(key)] = value

    return items


def normalise(curve: list):
    base_min_value = min(curve)
    base_max_value = max(curve)
    return [(value - base_min_value) / (base_max_value - base_min_value) for value in curve]


def scale_curve(reference_curve: list, target_length: int):
    # -> Generate curve
    x = np.linspace(0, 1, len(reference_curve))
    y = np.array(reference_curve)

    f = np.polynomial.polynomial.Polynomial.fit(x, y, len(reference_curve) - 1)
    # f = np.poly1d(np.polyfit(x, y, len(normalized_curve) - 1))
    x_new = np.linspace(0.1, 1, target_length)
    return f(x_new).tolist()


def generate_curve(reference_curve: list, target_length: int, min_value: float, max_value: float):
    # -> Normalize reference curve
    normalized_curve = normalise(curve=reference_curve)

    # -> Generate curve
    y_new = scale_curve(
        reference_curve=normalized_curve,
        target_length=target_length
    )

    # -> Normalize generated curve
    y_new_normalized = normalise(curve=y_new)

    # -> Scale curve
    y_new_scaled = [value * (max_value - min_value) + min_value for value in y_new_normalized]

    return y_new_scaled


if __name__ == "__main__":
    reference_list = [-1, 2, 3, 4, 5, 3, 2, 4, 5, 7]
    reference_list = [10, 10]
    length = 100

    # -> Plot generated curve
    plt.plot(scale_curve(reference_list, length))
    plt.show()

    dataDict = {
        "a": 1,
        "bfsadf": {
            "cncvb": 2,
            "djkhl": {
                "e": 3,
                "f": 4
            }
        }
    }

    print(flatten_dict(dataDict))