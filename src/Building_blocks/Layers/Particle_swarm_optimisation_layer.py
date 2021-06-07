
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
                 verbose=0):
        super().__init__()

        self.layer_ref = None
        self.layer_type = "PSO_layer"

        self.parameter_randomiser = parameter_randomiser

        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

        self.parameter_blacklist = parameter_blacklist
        self.parameters_decay_function = parameters_decay_function

        self.verbose = verbose

        return

    def __str__(self):

        return f"> {self.layer_type} - " \
               f"Inertia weight: {self.inertia_weight}, " \
               f"Cognitive weight: {self.cognitive_weight}, " \
               f"Social weight: {self.social_weight}"

    def step(self, population, evaluation_function, epoch, max_epoch):
        # --> Evaluate population
        fitness_evaluation = population.get_fitness_evaluation(evaluation_function)

        # Find pop max fitness index
        swarm_max_fitness_index = fitness_evaluation.index(max(fitness_evaluation))

        # Determine individual parameters difference percentage between pop max fitness sol and all other sol


        # Solve for

        if self.verbose == 1:
            print(f"---- << PSO layer >> ----")
            print(f" Inertia weight: {self.inertia_weight}")
            print(f" Cognitive weight: {self.cognitive_weight}")
            print(f" Social weight: {self.social_weight}")
            print("\n")

        return population
