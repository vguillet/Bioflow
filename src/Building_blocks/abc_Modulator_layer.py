
################################################################################################################
"""
Ensure that the new population is an edited version of the old one
or the new population is a Population class instance
"""

# Built-in/Generic Imports
import json
import random
from abc import ABC, abstractmethod

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class Modulator_layer(ABC):
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
        # -> Meta
        self.ref = ""
        self.type = "Unknown"
        self.name = name

        self.verbose = verbose

        # -> Settings
        self.param = {
            "evaluation_function": evaluation_function,
            "evaluation_function_epoch_trigger": evaluation_function_epoch_trigger,
            "evaluation_function_trigger_mode": evaluation_function_trigger_mode,

            "data": data,
            "data_epoch_trigger": data_epoch_trigger,
            "data_trigger_mode": data_trigger_mode,

            "settings": settings,
            "settings_epoch_trigger": settings_epoch_trigger,
            "settings_trigger_mode": settings_trigger_mode,
        }

    @abstractmethod
    def __str__(self):
        return

    def prime(self, epochs: int) -> bool:

        # -> Iterate through all weights and generate curves if reference curve is not None
        for weight_type in self.param["base_weights"].keys():
            if self.param["weight_curves"][weight_type]["reference_curve"] is not None:
                self.param["weight_curves"][weight_type]["scaled_curve"] = scale_curve(
                    reference_curve=self.param["weight_curves"][weight_type]["reference_curve"],
                    target_length=epochs
                )

        return True

    def get_epoch_weights(self, epoch: int) -> dict:
        """
        Get the weights for the current epoch

        :param epoch:
        :return:
        """

        weights = {}

        # -> Retrieve weights for current epoch
        for weight_type in self.param["base_weights"].keys():
            if self.param["weight_curves"][weight_type]["reference_curve"] is not None:
                weights[weight_type] = self.param["weight_curves"][weight_type]["scaled_curve"][epoch]
            else:
                weights[weight_type] = self.param["base_weights"][weight_type]

        return weights

    @abstractmethod
    def step(self, population, evaluation_function, epoch, data=None, settings=None):
        return population
