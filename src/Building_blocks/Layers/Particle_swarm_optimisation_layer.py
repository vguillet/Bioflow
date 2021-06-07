
################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
import random

# Libs

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer
from src.Tools.Parameter_tools import select_parameter_to_modify
from src.Building_blocks.Population import Population


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class PSO_Layer(Layer):
    def __init__(self,
                 parameter_randomiser,

                 inertia_weight: float,
                 cognitive_weight: float,       # Particle best influence
                 social_weight: float,          # Swarm overall best influence

                 parameter_blacklist: list = [],
                 parameters_decay_function: int = 0,

                 optimisation_mode="max",
                 verbose=0,
                 name=""):
        super().__init__(name=name)

        self.layer_type = "PSO_layer"
        self.verbose = verbose
        self.optimisation_mode = optimisation_mode

        self.parameter_randomiser = parameter_randomiser

        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

        self.parameter_blacklist = parameter_blacklist
        self.parameters_decay_function = parameters_decay_function

        return

    def __str__(self):
        if self.layer_name != "":
            layer_name = f"{self.layer_name} - "
        else:
            layer_name = ""

        return f"> {self.layer_type} - " + layer_name + \
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

        # --> Determine individual parameters difference percentage between pop max fitness sol and all other sol
        for individual in population:
            for key in individual.parameter_set.keys():
                individual_best_param_diff = (individual.best_parameter_set[key] - individual.parameter_set[key])
                swarm_max_param_diff = (swarm_best_fitness_parameter_set[key] - individual.best_parameter_set[key])

                particle_velocity = self.inertia_weight * individual.velocity_history[-1] \
                                    + self.cognitive_weight * random.random() * individual_best_param_diff \
                                    + self.social_weight * random.random() * swarm_max_param_diff

                individual.parameter_set[key] += particle_velocity

        if self.verbose == 1:
            print(f"---- << PSO layer >> ----")
            print(f" Inertia weight: {self.inertia_weight}")
            print(f" Cognitive weight: {self.cognitive_weight}")
            print(f" Social weight: {self.social_weight}")
            print("\n")

        return population
