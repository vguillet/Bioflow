
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import numpy as np
import matplotlib.pyplot as plt

# Own modules
from src.Building_blocks.Functional_layers.Step_layer import STEP_layer
from Test_cases.Rastrigin.Rastrigin_Individual import Rastrigin_Indvidual
from Test_cases.Rastrigin.Rastrigin_function import Rastrigin_function


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Rastrigin_VISU_layer(STEP_layer):
    def __init__(self,
                 plot_rate=10,
                 name="Visualiser"):

        super().__init__(name=name, verbose=0)

        self.plot_rate = plot_rate

    def step(self, population, evaluation_function, optimisation_mode: int, epoch, data=None, settings=None):
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

            ax.view_init(elev=-90, azim=0)
            plt.show()

        return population


if __name__ == "__main__":
    my_solutions = []
    for _ in range(10):
        my_solutions.append(Rastrigin_Indvidual())

    Rastrigin_VISU_layer().step(my_solutions, "", 10, "")
