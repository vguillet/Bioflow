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
        super().__init__(name=name)

        self.layer_ref = "      "
        self.layer_type = "MODULATOR_layer"

        self.new_evaluation_function = new_evaluation_function
        self.new_step = new_step
        self.new_max_step = new_max_step

        self.verbose = verbose

        return

    def __str__(self):
        if self.layer_name != "":
            layer_name = f" - {self.layer_name}"
        else:
            layer_name = ""

        return f"> {self.layer_type}" + layer_name

    def step(self, population, evaluation_function, epoch, max_epoch):

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
