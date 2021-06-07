
################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys
import random
import json
from copy import deepcopy

# Libs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Own modules
from src.Building_blocks.Layers.Step_layer import STEP_layer
from src.Random.Rastrigin_Individual import Rastrigin_Indvidual
from src.Random.Rastrigin_function import Rastrigin_function


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Rastrigin_VISU_layer(STEP_layer):
    def __init__(self,
                 plot_rate=10,
                 name="Visualiser"):
        super().__init__(name=name)

        self.plot_rate = plot_rate

    def step(self, population, evaluation_function, epoch, max_epoch):
        if epoch % self.plot_rate == 0:
            x = np.linspace(-5.12, 5.12, 100)
            y = np.linspace(-5.12, 5.12, 100)
            x, y = np.meshgrid(x, y)

            z = (x ** 2 - 10 * np.cos(2 * np.pi * x)) + \
                (y ** 2 - 10 * np.cos(2 * np.pi * y)) + 20

            fig = plt.figure()
            ax = plt.axes(projection='3d')
            ax.plot_surface(x, y, z,
                            rstride=1, cstride=1,
                            cmap="Oranges", linewidth=0.01,
                            antialiased=True)

            x_population = []
            y_population = []
            z_population = []
            for individual in population:
                x_population.append(individual.parameter_set["x"])
                y_population.append(individual.parameter_set["y"])
                z_population.append(Rastrigin_function(individual))

            ax.scatter(x_population, y_population, z_population, color="blue")

            plt.show()

        return population


if __name__ == "__main__":
    my_solutions = []
    for _ in range(100):
        my_solutions.append(Rastrigin_Indvidual())

    Rastrigin_VISU_layer().step(my_solutions, "", 10, "")
