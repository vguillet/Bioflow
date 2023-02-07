
################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
import random

# Libs

# Own modules
from src.Building_blocks.Population import Population

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################

def gen_initial_population(individual_template, population_size=10):
    population_lst = Population()

    for i in range(population_size):
        population_lst.append(individual_template())

    return population_lst


def get_population_fitness_evaluation(population, evaluation_function):
    fitness_evaluation = []
    for individual in population:
        individual_fitness = evaluation_function(individual)

        individual.fitness_history.append(individual_fitness)
        fitness_evaluation.append(individual_fitness)

    return population, fitness_evaluation


def get_population_age(population):
    population_age = []

    for individual in population:
        population_age.append(len(individual.fitness_history))

    return population_age
