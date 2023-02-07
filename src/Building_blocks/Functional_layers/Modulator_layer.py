################################################################################################################
"""

"""

# Built-in/Generic Imports

# Own modules
from src.Building_blocks.abc_Modulator_layer import Modulator_layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class MODULATOR_layer(Modulator_layer):
    def __init__(self,
                 evaluation_function=None,
                 evaluation_function_epoch_trigger=None,
                 evaluation_function_trigger_mode: str = "threshold",

                 data=None,
                 data_epoch_trigger=None,
                 data_trigger_mode: str = "threshold",

                 settings=None,
                 settings_epoch_trigger=None,
                 settings_trigger_mode: str = "threshold",

                 verbose=0,
                 name=""):
        """
        Modulator layer, to be used to change the evaluation function, data, or settings of the model during training

        The trigger mode can be either "threshold" or "multiple".

        :param evaluation_function:
        :param evaluation_function_epoch_trigger:
        :param evaluation_function_trigger_mode: "threshold" or "multiple"
        :param data: Any
        :param data_epoch_trigger:
        :param data_trigger_mode: "threshold" or "multiple"
        :param settings: Any
        :param settings_epoch_trigger:
        :param settings_trigger_mode: "threshold" or "multiple"
        :param verbose: int
        :param name: str
        """

        super().__init__(
            evaluation_function=evaluation_function,
            evaluation_function_epoch_trigger=evaluation_function_epoch_trigger,
            evaluation_function_trigger_mode=evaluation_function_trigger_mode,

            data=data,
            data_epoch_trigger=data_epoch_trigger,
            data_trigger_mode=data_trigger_mode,

            settings=settings,
            settings_epoch_trigger=settings_epoch_trigger,
            settings_trigger_mode=settings_trigger_mode,

            verbose=verbose,
            name=name
        )

        # -> Meta
        self.type = "MODULATOR"

    def __str__(self):
        return f"  -> {self.name} ({self.type})"

    def step(self, evaluation_function, data=None, settings=None):

        if self.new_evaluation_function is not None:
            evaluation_function = self.new_evaluation_function

        if self.verbose == 1:
            print(f"---- << MODULATOR layer >> ----")
            if self.new_evaluation_function is not None:
                print(f" Set evaluation function: {self.new_evaluation_function}")

            print("\n")

        return evaluation_function
