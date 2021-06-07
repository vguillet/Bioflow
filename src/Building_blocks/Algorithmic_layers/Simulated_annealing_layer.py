
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Building_blocks.abc_Layer import Layer

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
        self.type = "SA"
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
        return f"       {self.name} ({self.type})         " + \
               f"Inertia weight: {self.inertia_weight}, " \
               f"Cognitive weight: {self.cognitive_weight}, " \
               f"Social weight: {self.social_weight}"

    def step(self, population, evaluation_function, epoch, max_epoch, data=None, settings=None):
        # --> Evaluate population (record fitness of population)
        population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                          data=data,
                                          optimisation_mode=self.optimisation_mode)

        if self.verbose == 1:
            print(f"---- << SA layer >> ----")
            print(f" Inertia weight: {self.inertia_weight}")
            print(f" Cognitive weight: {self.cognitive_weight}")
            print(f" Social weight: {self.social_weight}")
            print("\n")

        return population
