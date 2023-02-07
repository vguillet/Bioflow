################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Building_blocks.abc_Layer import Layer
from src.Tools.Parameter_tools import *

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class PSO_Layer(Layer):
    def __init__(self,
                 # Weights
                 inertia_weight: int or float or list = 0.729,
                 cognitive_weight: int or float or list = 1.49445,  # Particle best influence
                 social_weight: int or float or list = 1.49445,  # Swarm overall best influence

                 # Blacklisted parameters
                 parameter_blacklist: list = [],

                 # Misc settings
                 optimisation_mode="max",
                 evaluation_function=None,
                 verbose=0,
                 name="Layer"):
        """
        Initialise a PSO layer.

        :param inertia_weight:
        :param cognitive_weight:
        :param social_weight:
        :param inertia_weight_curve:
        :param cognitive_weight_curve:
        :param social_weight_curve:
        :param parameter_blacklist:
        :param optimisation_mode:
        :param verbose:
        :param name:
        """

        super().__init__(name=name, verbose=verbose)

        # -> Meta
        self.type = "PSO"

        # -> Settings
        self.param = {
            # Weight curves
            "weight_curves": {
                "inertia_weight": {
                    "reference_curve": inertia_weight if isinstance(inertia_weight, list)
                                        else [inertia_weight, inertia_weight],
                    "scaled_curve": None,
                },

                "cognitive_weight": {
                    "reference_curve": cognitive_weight if isinstance(cognitive_weight, list)
                                        else [cognitive_weight, cognitive_weight],
                    "scaled_curve": None,
                },

                "social_weight": {
                    "reference_curve": social_weight if isinstance(social_weight, list)
                                        else [social_weight, social_weight],
                    "scaled_curve": None,
                },

            },

            # Blacklist
            "parameter_blacklist": parameter_blacklist,

            # Misc
            "optimisation_mode": optimisation_mode,
            "evaluation_function": evaluation_function,
        }

        return

    def __str__(self):
        """
        Print layer information
        :return: String
        """

        # -> Construct layer info
        layer_info = f"-------------- {self.name} ({self.type})        "
        layer_info += self.weights_summary()

        return layer_info

    def step(self, population, evaluation_function, epoch: int, data=None, settings=None):
        """
        Perform a single step of the PSO algorithm

        :param population: Population to step
        :param evaluation_function: Function to evaluate the fitness of the population
        :param epoch: Current epoch
        :param data:
        :param settings:
        :return: Population after step
        """

        # -> Get epoch weights
        epoch_weights = self.get_epoch_weights(epoch=epoch)

        # ============================================================== Evaluate population
        # !!! Evaluation function set in layer is always prioritised over evaluation function provided by model !!!
        if self.param["evaluation_function"] is not None:
            evaluation_function = self.param["evaluation_function"]

        population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                          data=data,
                                          optimisation_mode=self.param['optimisation_mode'])

        # ============================================================== Prepare population
        # -> Add velocity property to individuals if missing
        for individual in population:
            if not hasattr(individual, "velocity"):
                individual.velocity_history = [0]

        # -> Find pop max fitness index
        swarm_best_fitness_parameter_set = population.best_individual_history[-1].parameter_set

        # ============================================================== Update population
        # -> Get parameter key map
        key_map = flatten_dict(deepcopy(population[0].parameter_set))

        for individual in population:

            # -> Adjust all non-blacklisted parameters
            for key in key_map:
                key = list(key)

                if any(item in key for item in self.param['parameter_blacklist']) is False:
                    # -> Get difference between best swarm fitness and current fitness
                    individual_best_param_diff = get_from_dict(individual.best_parameter_set, key) \
                                                 - get_from_dict(individual.parameter_set, key)

                    # -> Get difference between best individual fitness and current fitness
                    swarm_max_param_diff = get_from_dict(swarm_best_fitness_parameter_set, key) \
                                           - get_from_dict(individual.best_parameter_set, key)

                    # -> Solve for velocity
                    particle_velocity = epoch_weights['inertia_weight'] * individual.velocity_history[-1] \
                                        + epoch_weights['cognitive_weight'] * random.random() * individual_best_param_diff \
                                        + epoch_weights['social_weight'] * random.random() * swarm_max_param_diff

                    # -> Apply movement
                    add_in_dict(individual.parameter_set, list(key), particle_velocity)

                else:
                    pass

        # ============================================================== Print step info
        if self.verbose == 1:
            print(f"---- << PSO layer >> ----")
            print(f" Inertia weight: {epoch_weights['inertia_weight']}")
            print(f" Cognitive weight: {epoch_weights['cognitive_weight']}")
            print(f" Social weight: {epoch_weights['social_weight']}")
            print("\n")

        return population
