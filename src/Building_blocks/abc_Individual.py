################################################################################################################
"""

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


class Individual(ABC):
    def __init__(self):

        self.parameter_set = None

        self.parameter_blacklist = []

        self.fitness_history = []
        self.parameter_set_history = []

        return

    def get_adjustable_parameter_count(self, layer_parameter_blacklist: list = []):
        # -> Merge individual parameter blacklist with layer parameter blacklist
        parameter_blacklist = (self.parameter_blacklist + layer_parameter_blacklist)

        parameter_dict_flat = flatten_dict(self.parameter_set)

        # -> Count all parameters that do not contain a key in the blacklist
        adjustable_parameter_count = 0

        for parameter in parameter_dict_flat:
            if not any(key in parameter for key in parameter_blacklist):
                adjustable_parameter_count += 1

        return adjustable_parameter_count

    @property
    def best_fitness(self):
        return max(self.fitness_history)

    @property
    def best_parameter_set(self):
        max_fitness_index = self.fitness_history.index(self.best_fitness)
        return self.parameter_set_history[max_fitness_index]

    @abstractmethod
    def gen_parameter_set(self):
        return

    def get_fitness_evaluation(self,
                               evaluation_function,
                               data,
                               settings,
                               record_evaluation=False):
        """
        Evaluate the individual's fitness.

        :param evaluation_function: Function to evaluate individuals
        :param data: Data to evaluate individuals on
        :param settings: Settings to pass to the layer
        :param record_evaluation: Whether to record the evaluation in the individual's history

        :return: Fitness value
        """

        # -> Evaluate individual
        individual_fitness = evaluation_function(
            individual=self,
            data=data,
            settings=settings
        )

        # -> Record to individual history
        if record_evaluation:
            self.fitness_history.append(individual_fitness)
            self.parameter_set_history.append(self.parameter_set)

        return individual_fitness
