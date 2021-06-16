################################################################################################################
"""

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


class Individual(ABC):
    def __init__(self):

        self.nb_of_adjustable_parameters = 0
        self.parameter_set = None

        self.fitness_history = []
        self.parameter_set_history = []

        return

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
                               record_evaluation=False,
                               optimisation_mode="max"):
        # --> Evaluate individual
        individual_fitness = evaluation_function(individual=self,
                                                 data=data)

        # --> Record to individual history
        if record_evaluation:
            self.fitness_history.append(individual_fitness)
            self.parameter_set_history.append(self.parameter_set)

        return individual_fitness
