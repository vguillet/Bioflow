
################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
import random

# Libs

# Own modules
from src.Tools.Population_tools import get_population_fitness_evaluation
from src.Tools.Population_tools import get_population_age


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################

class Population(list):
    best_fitness_history = []
    best_individual_history = []

    def get_fitness_evaluation(self, evaluation_function):
        fitness_evaluation = []
        for individual in self:
            individual_fitness = evaluation_function(individual)

            individual.fitness_history.append(individual_fitness)
            fitness_evaluation.append(individual_fitness)

            # --> Record solution if best overall
            if len(self.best_fitness_history) == 0 or individual_fitness > self.best_fitness_history[-1]:
                self.best_fitness_history.append(individual_fitness)
                self.best_individual_history.append(individual)

        return fitness_evaluation

    def get_individual_ages(self):
        population_age = []

        for individual in self:
            population_age.append(len(individual.fitness_history))

        return population_age
