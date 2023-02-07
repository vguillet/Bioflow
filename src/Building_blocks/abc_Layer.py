
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
from src.Tools.Parameter_tools import *

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class Layer(ABC):
    def __init__(self,
                 name="",
                 verbose=0):
        # -> Meta
        self.ref = ""
        self.type = "Unknown"
        self.name = name

        self.verbose = verbose

        # -> Settings
        self.param = {
            "weight_curves": {},
        }

    @abstractmethod
    def __str__(self):
        return

    def weights_summary(self):
        """
        Return a string summarising the weights of the layer

        :return: str
        """

        layer_weights_info = ""
        weights = {}

        # -> Get weights definition
        for weight_type in self.param["weight_curves"].keys():
            if len(self.param["weight_curves"][weight_type]["reference_curve"]) != 2:
                weights[weight_type] = \
                    f"Curve (min: {min(self.param['weight_curves'][weight_type]['reference_curve'])}, " \
                    f"max: {max(self.param['weight_curves'][weight_type]['reference_curve'])})"

            else:
                weights[weight_type] = self.param["weight_curves"][weight_type]["reference_curve"][0]

        # -> Format weights definition
        for weight_type in weights.keys():
            layer_weights_info += f"\n     - {weight_type}: {weights[weight_type]}"

        return layer_weights_info

    def prime(self, epochs: int) -> bool:
        """
        Generate the weight curves for the layer

        :param epochs:
        :return:
        """

        # -> Iterate through all weights and generate curves if reference curve is not None
        for weight_type in self.param["weight_curves"].keys():
            self.param["weight_curves"][weight_type]["scaled_curve"] = \
                scale_curve(reference_curve=self.param["weight_curves"][weight_type]["reference_curve"],
                            target_length=epochs)

        # -> If parameters_throttle_curves is defined, scale each parameter curve
        if "parameters_throttle_curves" in self.param.keys():

            if self.param["parameters_throttle_curves"] is not None:
                # -> Iterate through all parameters and generate corresponding scaled curves
                for parameter in self.param["parameters_throttle_curves"].keys():
                    self.param["parameters_throttle_curves_scaled"][parameter] = \
                        scale_curve(reference_curve=self.param["parameters_throttle_curves"][parameter],
                                    target_length=epochs)

        return True

    def get_epoch_weights(self, epoch: int) -> dict:
        """
        Get the weights for the current epoch

        :param epoch:
        :return:
        """

        weights = {}

        # -> Retrieve weights for current epoch
        for weight_type in self.param["weight_curves"].keys():
            weights[weight_type] = self.param["weight_curves"][weight_type]["scaled_curve"][epoch]

        return weights

    @abstractmethod
    def step(self, population, evaluation_function, optimisation_mode: str, epoch: int, data=None, settings=None):
        return population
