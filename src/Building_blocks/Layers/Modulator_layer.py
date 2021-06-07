################################################################################################################
"""

"""

# Built-in/Generic Imports

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class MODULATOR_layer(Layer):
    def __init__(self,
                 new_evaluation_function=None,
                 new_step=None,
                 new_max_step=None,
                 verbose=0,
                 name=""):

        # --> Meta
        self.ref = "      "
        self.type = "MODULATOR"
        self.name = name

        self.verbose = verbose

        # --> Settings
        self.new_evaluation_function = new_evaluation_function
        self.new_step = new_step
        self.new_max_step = new_max_step

        return

    def __str__(self):
        return f"  -> {self.name} ({self.type})"

    def step(self, population, evaluation_function, epoch, max_epoch, data=None):

        if self.new_evaluation_function is not None:
            evaluation_function = self.new_evaluation_function

        if self.new_step is not None:
            epoch = self.new_step

        if self.new_max_step is not None:
            max_epoch = self.new_max_step

        if self.verbose == 1:
            print(f"---- << MODULATOR layer >> ----")
            if self.new_evaluation_function is not None:
                print(f" Set evaluation function: {self.new_evaluation_function}")

            if self.new_step is not None:
                print(f" Set step: {self.new_step}")

            if self.new_max_step is not None:
                print(f" Set max step: {self.new_max_step}")

            print("\n")

        return population, evaluation_function, epoch, max_epoch
