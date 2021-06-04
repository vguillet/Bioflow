
################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys
import random
import json
from copy import deepcopy

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer
from src.Tools.Parameter_tools import select_parameter_to_modify

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class EVO_layer(Layer):
    def __init__(self,
                 individual_template,
                 parameter_randomiser,
                 percent_parents: int = 0.3,
                 percent_parents_in_next_gen: int = 0.1,
                 percent_random_ind_in_next_gen: float = 0.1,
                 mutation_rate: float = 0.2,
                 selection_method: int = 0,
                 parameter_blacklist: list = [],
                 parameters_decay_function: int = 0):
        super().__init__()

        self.layer_type = "EVO_layer"

        self.individual_template = individual_template
        self.parameter_randomiser = parameter_randomiser

        self.percent_parents = percent_parents
        self.percent_parents_in_next_gen = percent_parents_in_next_gen
        self.percent_random_ind_in_next_gen= percent_random_ind_in_next_gen
        self.mutation_rate = mutation_rate
        self.selection_method = selection_method
        self.parameter_blacklist = parameter_blacklist
        self.parameters_decay_function = parameters_decay_function

        return

    def __str__(self):
        settings_option_lists = json.load(open(r"src/Configuration_management/Settings_option_list.json"))
        selection_method = settings_option_lists["parents_selection_methods"][self.selection_method]

        return f"> {self.layer_type} - " \
               f"Parents: {self.percent_parents * 100}%, " \
               f"Parents in next gen: {self.percent_parents_in_next_gen * 100}%, " \
               f"Random: {self.percent_random_ind_in_next_gen * 100}%, " \
               f"Mutation rate: {self.mutation_rate * 100}, " \
               f"Selection method: {selection_method}"

    def step(self, population, evaluation_function, epoch, max_epoch):
        # --> Evaluate population
        fitness_evaluation = []
        for individual in population:
            fitness_evaluation.append(evaluation_function(individual))

        assert(len(fitness_evaluation) == len(population))

        # --> Generate new population
        new_population = self.evolve_population(parameter_randomiser=self.parameter_randomiser,
                                                epoch=epoch,
                                                max_epoch=max_epoch,
                                                population=population,
                                                fitness_evaluation=fitness_evaluation,
                                                parents_count=round(len(population) * self.percent_parents),
                                                parents_count_in_next_gen=round(len(population) * self.percent_parents_in_next_gen),
                                                random_ind_count_in_next_gen=round(len(population) * self.percent_random_ind_in_next_gen),
                                                mutation_rate=self.mutation_rate,
                                                selection_method=self.selection_method,
                                                parameter_blacklist=self.parameter_blacklist,
                                                parameters_decay_function=self.parameters_decay_function)

        return new_population

    def evolve_population(self,
                          epoch: int,
                          max_epoch: int,
                          population: list,
                          fitness_evaluation: list,
                          parents_count: int,
                          parents_count_in_next_gen: int,
                          random_ind_count_in_next_gen: int,
                          mutation_rate: float,
                          selection_method: int,
                          parameter_blacklist: list,
                          parameter_randomiser,
                          parameters_decay_function: int):
        # ----- Select parents
        parents = []
        # --> Determine fitness ratio
        fitness_ratios = []
        for i in range(len(fitness_evaluation)):
            fitness_ratios.append(fitness_evaluation[i] / sum(fitness_evaluation) * 100)

        # --> Select individuals
        # TODO: Implement alternative selection methods
        # Elitic selection
        if selection_method == 0:
            # Use bubblesort to sort population, fitness_evaluation, and fitness_ratios according to fitness_ratio
            for _ in range(len(fitness_ratios)):
                for i in range(len(fitness_ratios) - 1):
                    if fitness_ratios[i] < fitness_ratios[i + 1]:
                        fitness_ratios[i], fitness_ratios[i + 1] = fitness_ratios[i + 1], fitness_ratios[i]
                        population[i], population[i + 1] = population[i + 1], population[i]
                        fitness_evaluation[i], fitness_evaluation[i + 1] = fitness_evaluation[i + 1], fitness_evaluation[i]

            for i in range(parents_count):
                parents.append(population[i])

        # --> Exit program if incorrect settings used
        else:
            sys.exit("Invalid parent selection method reference")

        # ----- Generate new population
        # TODO: Throttle number of parameters to mutate
        nb_of_parameters_to_mutate = round(parents[0].nb_of_adjustable_parameters * mutation_rate) or 1

        # --> Add required number of parents to new population (from best to worst)
        new_population = parents[:parents_count_in_next_gen]

        # --> Generate offsprings from parents with mutations
        # Cycle through parent list to create offspring
        cycling = -1
        for _ in range(len(population) - parents_count_in_next_gen - random_ind_count_in_next_gen):
            cycling += 1
            if cycling >= len(parents):
                cycling = 0

            offspring = deepcopy(parents[cycling])

            # Mutate offspring
            for _ in range(nb_of_parameters_to_mutate):
                # Select parameter class to modify
                parameter_to_modify = select_parameter_to_modify(parameter_set=offspring.parameter_set.keys(),
                                                                 parameter_blacklist=parameter_blacklist)

                # Modify parameter
                offspring = parameter_randomiser().modify_param(offspring=offspring,
                                                                parameter_to_modify=parameter_to_modify,
                                                                current_generation=epoch,
                                                                nb_of_generations=max_epoch,
                                                                parameters_decay_function=parameters_decay_function)

            # Add offspring to new population
            new_population.append(offspring)

        # --> Create random_ind number of random individuals and add to new population
        for _ in range(random_ind_count_in_next_gen):
            new_population.append(deepcopy(self.individual_template()))

        assert (len(new_population) == len(population))

        return new_population
