
################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
import random
from copy import deepcopy

# Libs
from flatten_dict import flatten
from flatten_dict import unflatten

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer
from src.Tools.Parameter_tools import select_random_parameter_to_modify, get_from_dict, add_in_dict
from src.Building_blocks.Population import Population


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class PSO_Layer(Layer):
    def __init__(self,
                 parameter_randomiser,

                 inertia_weight: float = 0.729,
                 cognitive_weight: float = 1.49445,       # Particle best influence
                 social_weight: float = 1.49445,          # Swarm overall best influence

                 parameter_blacklist: list = [],
                 parameters_decay_function: int = 0,

                 optimisation_mode="max",
                 verbose=0,
                 name="Layer"):
        # --> Meta
        self.ref = ""
        self.type = "PSO"
        self.name = name

        self.verbose = verbose
        self.optimisation_mode = optimisation_mode

        # --> Settings
        self.parameter_randomiser = parameter_randomiser

        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

        self.parameter_blacklist = parameter_blacklist
        self.parameters_decay_function = parameters_decay_function

        return

    def __str__(self):
        return f"       {self.name} ({self.type})        " + \
               f"Inertia weight: {self.inertia_weight}, " \
               f"Cognitive weight: {self.cognitive_weight}, " \
               f"Social weight: {self.social_weight}"

    def step(self, population, evaluation_function, epoch, max_epoch):
        # --> Evaluate population (record fitness of population)
        population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                          optimisation_mode=self.optimisation_mode)

        # --> Add velocity property to individuals if missing
        for individual in population:
            if not hasattr(individual, "velocity"):
                individual.velocity_history = [0]

        # --> Find pop max fitness index
        swarm_best_fitness_parameter_set = population.best_individual_history[-1].parameter_set

        # --> Get parameter key map
        key_map = flatten(deepcopy(population[0].parameter_set))

        for individual in population:
            for key in key_map:
                key = list(key)

                if any(item in key for item in self.parameter_blacklist) is False:
                    # --> Get difference between best swarm fitness and current fitness
                    individual_best_param_diff = get_from_dict(individual.best_parameter_set, key) \
                                                 - get_from_dict(individual.parameter_set, key)

                    # --> Get difference between best individual fitness and current fitness
                    swarm_max_param_diff = get_from_dict(swarm_best_fitness_parameter_set, key) \
                                           - get_from_dict(individual.best_parameter_set, key)

                    # --> Solve for velocity
                    particle_velocity = self.inertia_weight * individual.velocity_history[-1] \
                                        + self.cognitive_weight * random.random() * individual_best_param_diff \
                                        + self.social_weight * random.random() * swarm_max_param_diff

                    # --> Apply movement
                    add_in_dict(individual.parameter_set, list(key), particle_velocity)

                else:
                    pass

        if self.verbose == 1:
            print(f"---- << PSO layer >> ----")
            print(f" Inertia weight: {self.inertia_weight}")
            print(f" Cognitive weight: {self.cognitive_weight}")
            print(f" Social weight: {self.social_weight}")
            print("\n")

        return population
