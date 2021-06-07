
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
from src.Building_blocks.Population import Population
from src.Tools.Parameter_tools import select_parameter_to_modify


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class EVO_layer(Layer):
    def __init__(self,
                 parameter_randomiser,

                 individual_template,
                 percent_parents: float = 0.3,
                 percent_parents_in_next_gen: float = 0.1,
                 percent_random_ind_in_next_gen: float = 0.1,
                 selection_method: int = 0,

                 mutation_rate: float = 0.2,
                 parameter_blacklist: list = [],
                 parameters_decay_function: int = 0,

                 optimisation_mode="max",
                 verbose=0,
                 name="Layer"):
        # --> Meta
        self.ref = ""
        self.type = "EVO"
        self.name = name

        self.verbose = verbose
        self.optimisation_mode = optimisation_mode

        # --> Settings
        self.parameter_randomiser = parameter_randomiser

        self.individual_template = individual_template
        self.percent_parents = percent_parents
        self.percent_parents_in_next_gen = percent_parents_in_next_gen
        self.percent_random_ind_in_next_gen = percent_random_ind_in_next_gen
        self.selection_method = selection_method
        self.mutation_rate = mutation_rate

        self.parameter_blacklist = parameter_blacklist
        self.parameters_decay_function = parameters_decay_function

        return

    def __str__(self):

        settings_option_lists = json.load(open(r"src/Configuration_management/Settings_option_list.json"))
        selection_method = settings_option_lists["parents_selection_methods"][self.selection_method]

        return f"       {self.name} ({self.type})        " + \
               f"Optimiser mode: {self.optimisation_mode}, " \
               f"Parents: {self.percent_parents * 100}%, " \
               f"Parents in next gen: {self.percent_parents_in_next_gen * 100}%, " \
               f"Random: {self.percent_random_ind_in_next_gen * 100}%, " \
               f"Mutation rate: {self.mutation_rate * 100}, " \
               f"Selection method: {selection_method}"

    def step(self, population, evaluation_function, epoch, max_epoch):

        # --> Evaluate population
        fitness_evaluation = population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                                               optimisation_mode=self.optimisation_mode)

        parents_count = round(len(population) * self.percent_parents)
        parents_count_in_next_gen = round(len(population) * self.percent_parents_in_next_gen)
        random_ind_count_in_next_gen = round(len(population) * self.percent_random_ind_in_next_gen)

        assert len(population) >= parents_count_in_next_gen + random_ind_count_in_next_gen, \
            "!!! Sum of desired parent count and random individual count larger than total population size !!!"

        # ----- Select parents
        parents = []

        # --> Select individuals
        # TODO: Implement alternative selection methods
        # Elitic selection
        if self.selection_method == 0:
            # Use bubblesort to sort population and fitness_evaluation according to fitness_evaluation
            for _ in range(len(fitness_evaluation)):
                for i in range(len(fitness_evaluation) - 1):
                    if self.optimisation_mode == "max":         # -> Sorting from large to small
                        if fitness_evaluation[i] < fitness_evaluation[i + 1]:
                            # Reorder population
                            population[i], population[i + 1] = population[i + 1], population[i]

                            # Reorder fitness evaluation
                            fitness_evaluation[i], fitness_evaluation[i + 1] = fitness_evaluation[i + 1], fitness_evaluation[i]

                    elif self.optimisation_mode == "min":       # -> Sorting from small to large
                        if fitness_evaluation[i] > fitness_evaluation[i + 1]:
                            # Reorder population
                            population[i], population[i + 1] = population[i + 1], population[i]

                            # Reorder fitness evaluation
                            fitness_evaluation[i], fitness_evaluation[i + 1] = fitness_evaluation[i + 1], fitness_evaluation[i]

                    else:
                        print("!!! Invalid Optimisation mode selected !!!")

            for i in range(parents_count):
                parents.append(population[i])

        # --> Exit program if incorrect settings used
        else:
            sys.exit("Invalid parent selection method reference")

        # ----- Generate new population
        # TODO: Throttle number of parameters to mutate
        nb_of_parameters_to_mutate = round(parents[0].nb_of_adjustable_parameters * self.mutation_rate) or 1

        # --> Add required number of parents to new population (from best to worst)
        new_population = Population(population[:parents_count_in_next_gen])

        # --> Generate offsprings from parents with mutations
        # Cycle through parent list to create offspring
        cycling = -1
        for _ in range(len(population) - parents_count_in_next_gen - random_ind_count_in_next_gen):
            cycling += 1
            if cycling >= len(parents):
                cycling = 0

            offspring = deepcopy(parents[cycling])

            # Reset offspring fitness history
            offspring.fitness_history = []

            # Mutate offspring
            for _ in range(nb_of_parameters_to_mutate):
                # Select parameter class to modify
                parameter_to_modify = select_parameter_to_modify(parameter_set=offspring.parameter_set,
                                                                 parameter_blacklist=self.parameter_blacklist)

                # Modify parameter
                offspring = self.parameter_randomiser().modify_param(offspring=offspring,
                                                                     parameter_to_modify=parameter_to_modify,
                                                                     current_generation=epoch,
                                                                     nb_of_generations=max_epoch,
                                                                     parameters_decay_function=self.parameters_decay_function)

            # Add offspring to new population
            new_population.append(offspring)

        # --> Create random_ind number of random individuals and add to new population
        for _ in range(random_ind_count_in_next_gen):
            new_population.append(deepcopy(self.individual_template()))

        if self.verbose == 1:
            print(f"---- << EVO layer {epoch + 1} >> ----")
            print(f" Parent count: {parents_count}")
            print(" Parents fitness:")
            for parent in parents:
                print(f"    > Fitness: {parent.fitness_history[-1]}, Age: {len(parent.fitness_history)}")

            print(f" Nb. parents in new population: {parents_count_in_next_gen}")
            print(f" Random individual in new population: {random_ind_count_in_next_gen}")
            print("\n")

        return new_population
