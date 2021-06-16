
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


class PSO_Layer(Layer):
    def __init__(self,
                 inertia_weight: float = 0.729,
                 cognitive_weight: float = 1.49445,       # Particle best influence
                 social_weight: float = 1.49445,          # Swarm overall best influence

                 parameter_blacklist: list = [],

                 optimisation_mode="max",
                 verbose=0,
                 name="Layer"):

        # --> Meta
        self.ref = ""
        self.type = "PSO"
        self.name = name

        self.verbose = verbose

        # --> Settings
        self.param = {"optimisation_mode": optimisation_mode,

                      "inertia_weight": inertia_weight,
                      "cognitive_weight": cognitive_weight,
                      "social_weight": social_weight,

                      "parameter_blacklist": parameter_blacklist
                      }

        return

    def __str__(self):
        return f"       {self.name} ({self.type})        " + \
               f"Inertia weight: {self.param['inertia_weight']}, " \
               f"Cognitive weight: {self.param['cognitive_weight']}, " \
               f"Social weight: {self.param['social_weight']}"

    def step(self, population, evaluation_function, epoch, max_epoch, data=None, settings=None):
        # --> Evaluate population (log fitness of population + best fitness)
        population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                          data=data,
                                          optimisation_mode=self.param['optimisation_mode'])

        # --> Add velocity property to individuals if missing
        for individual in population:
            if not hasattr(individual, "velocity"):
                individual.velocity_history = [0]

        # --> Find pop max fitness index
        swarm_best_fitness_parameter_set = population.best_individual_history[-1].parameter_set

        # --> Get parameter key map
        key_map = flatten(deepcopy(population[0].parameter_set))

        for individual in population:

            # --> Adjust all non-blacklisted parameters
            for key in key_map:
                key = list(key)

                if any(item in key for item in self.param['parameter_blacklist']) is False:
                    # --> Get difference between best swarm fitness and current fitness
                    individual_best_param_diff = get_from_dict(individual.best_parameter_set, key) \
                                                 - get_from_dict(individual.parameter_set, key)

                    # --> Get difference between best individual fitness and current fitness
                    swarm_max_param_diff = get_from_dict(swarm_best_fitness_parameter_set, key) \
                                           - get_from_dict(individual.best_parameter_set, key)

                    # --> Solve for velocity
                    particle_velocity = self.param['inertia_weight'] * individual.velocity_history[-1] \
                                        + self.param['cognitive_weight'] * random.random() * individual_best_param_diff \
                                        + self.param['social_weight'] * random.random() * swarm_max_param_diff

                    # --> Apply movement
                    add_in_dict(individual.parameter_set, list(key), particle_velocity)

                else:
                    pass

        if self.verbose == 1:
            print(f"---- << PSO layer >> ----")
            print(f" Inertia weight: {self.param['inertia_weight']}")
            print(f" Cognitive weight: {self.param['cognitive_weight']}")
            print(f" Social weight: {self.param['social_weight']}")
            print("\n")

        return population
