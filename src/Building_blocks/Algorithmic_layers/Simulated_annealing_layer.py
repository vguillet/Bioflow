
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from copy import deepcopy

# Libs
from flatten_dict import flatten

# Own modules
from src.Building_blocks.abc_Layer import Layer
from src.Building_blocks.Parameter_tools import get_from_dict, add_in_dict

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class SA_Layer(Layer):
    def __init__(self,
                 parameter_randomiser,

                 initial_temperature: float = 90,
                 final_temperature: float = 0.1,
                 alpha: float = 1,

                 parameter_blacklist: list = [],

                 optimisation_mode="max",
                 verbose=0,
                 name="Layer"):

        # --> Meta
        self.ref = ""
        self.type = "SA"
        self.name = name

        self.verbose = verbose

        # --> Settings
        self.param = {"optimisation_mode": optimisation_mode,
                      "parameter_randomiser": parameter_randomiser,

                      "initial_temperature": initial_temperature,
                      "final_temperature": final_temperature,
                      "alpha": alpha,

                      "parameter_blacklist": parameter_blacklist
                      }

        # self.parameter_randomiser = parameter_randomiser
        #
        # self.initial_temperature = initial_temperature
        # self.final_temperature = final_temperature
        # self.alpha = alpha
        #
        # self.parameter_blacklist = parameter_blacklist

        return

    def __str__(self):
        return f"       {self.name} ({self.type})         " + \
               f"Initial temperature: {self.param['initial_temperature']}, " \
               f"Final temperature: {self.param['final_temperature']}, " \
               f"Alpha temperature: {self.param['alpha']}"

    def step(self, population, evaluation_function, epoch, max_epoch, data=None, settings=None):
        # --> Evaluate population (record fitness of population)
        population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                          data=data,
                                          optimisation_mode=self.param['optimisation_mode'])

        # --> Get parameter key map
        key_map = flatten(deepcopy(population[0].parameter_set))

        for individual in population:

            # --> Create hypothetical individual
            temp_individual = deepcopy(individual)

            # --> Randomly adjust all non-blacklisted parameters
            for key in key_map:
                key = list(key)

                if any(item in key for item in self.parameter_blacklist) is False:

                    # --> Apply change
                    temp_individual = self.param['parameter_randomiser']().modify_param(offspring=temp_individual,
                                                                                        parameter_to_modify=parameter_to_modify,
                                                                                        current_generation=epoch,
                                                                                        nb_of_generations=max_epoch,
                                                                                        parameters_decay_function=self.param['parameters_decay_function'])

                    add_in_dict(temp_individual.parameter_set, list(key), random.random())

            # --> Evaluate new solution
            temp_individual_fitness = temp_individual.get_fitness_evaluation(evaluation_function=evaluation_function,
                                                                             data=data,
                                                                             optimisation_mode=self.optimisation_mode)
            # TODO: Finish layer logic
            # --> Accept new solution if better
            if temp_individual_fitness > individual.fitness_history[-1]:
                individual.parameter_set = temp_individual.parameter_set
            # --> Else, accept base don relative probability
            else:
                pass

        if self.verbose == 1:
            print(f"---- << SA layer >> ----")
            print(f" Inertia weight: {self.inertia_weight}")
            print(f" Cognitive weight: {self.cognitive_weight}")
            print(f" Social weight: {self.social_weight}")
            print("\n")

        return population
