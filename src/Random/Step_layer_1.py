
################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys
import random
import json
from copy import deepcopy

# Libs
import matplotlib.pyplot as plt

# Own modules
from src.Building_blocks.Layers.Step_layer import STEP_layer


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class STEP_layer_1(STEP_layer):
    def __init__(self):
        super().__init__()
        self.layer_type = "STEP_layer: Visualiser"

    def step(self, population, evaluation_function, epoch, max_epoch):
        if epoch % 10 == 0:
            x_lst = list(range(-1500, 1500))
            y_lst = []

            for x in x_lst:
                y_lst.append(-x ** 2)

            plt.plot(x_lst, y_lst)

            x_pop = []
            y_pop = []

            for individual in population:
                x_pop.append(individual.parameter_set["a"]
                             - individual.parameter_set["b"]
                             - 10 * individual.parameter_set["c"]
                             + 0 * individual.parameter_set["d"])

                y_pop.append(- (individual.parameter_set["a"]
                                - individual.parameter_set["b"]
                                - 10 * individual.parameter_set["c"]
                                + 0 * individual.parameter_set["d"]) ** 2)

            plt.scatter(x_pop, y_pop, color="orange")

            plt.show()
        return population
