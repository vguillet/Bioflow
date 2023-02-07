
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


class SA_Layer(Layer):
    def __init__(self,
                 # SA settings
                 parameter_randomiser,

                 # Weights
                 initial_temperature: float or list = 90,
                 final_temperature: float or list = 0.1,
                 alpha: float or list = 1,

                 parameters_throttle_curves: list or None = None,

                 # Blacklisted parameters
                 parameter_blacklist: list = [],

                 # Misc settings
                 optimisation_mode="max",
                 evaluation_function=None,
                 verbose=0,
                 name="Layer"):

        super().__init__(name=name, verbose=verbose)

        # --> Meta
        self.type = "SA"

        # --> Settings
        self.param = {
            # SA settings
            "parameter_randomiser": parameter_randomiser,

            # Weight curves
            "weight_curves": {
                "initial_temperature": {
                    "reference_curve": initial_temperature if type(initial_temperature) is list
                    else [initial_temperature, initial_temperature],
                    "scaled_curve": None,
                },

                "final_temperature": {
                    "reference_curve": final_temperature if type(final_temperature) is list
                    else [final_temperature, final_temperature],
                    "scaled_curve": None,
                },

                "alpha": {
                    "reference_curve": alpha if type(alpha) is list
                    else [alpha, alpha],
                    "scaled_curve": None,
                },

                "parameters_throttle_curves": {
                    "reference_curve": parameters_throttle_curves if isinstance(parameters_throttle_curves, list)
                                        else [parameters_throttle_curves, parameters_throttle_curves],
                    "scaled_curve": None,
                },
            },

            # Blacklist
            "parameter_blacklist": parameter_blacklist,

            # Misc
            "optimisation_mode": optimisation_mode,
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
        """
        :return: String representation of layer
        """

        # -> Construct layer info
        layer_info = f"-------------- {self.name} ({self.type})        " + \
                     f"\n     - Optimiser mode: {self.param['optimisation_mode']} " + \
                     f"\n     - Selection method: {self.param['selection_method']} \n"
        layer_info += self.weights_summary()

        return layer_info

    def step(self, population, evaluation_function, epoch, data=None, settings=None):
        # -> Get epoch weights
        epoch_weights = self.get_epoch_weights(epoch=epoch)

        # --> Evaluate population (record fitness of population)
        # !!! Evaluation function set in layer is always prioritised over evaluation function provided by model !!!
        if self.param["evaluation_function"] is not None:
            evaluation_function = self.param["evaluation_function"]

        population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                          data=data,
                                          optimisation_mode=self.param['optimisation_mode'])

        # --> Get parameter key map
        key_map = flatten_dict(dataDict=deepcopy(population[0].parameter_set))

        for individual in population:

            # --> Create hypothetical individual
            temp_individual = deepcopy(individual)

            # --> Randomly adjust all non-blacklisted parameters
            for key in key_map:
                key = list(key)

                if any(item in key for item in self.parameter_blacklist) is False:

                    # --> Apply change
                    temp_individual = self.param['parameter_randomiser'](offspring=temp_individual,
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
            # --> Else, accept based on relative probability
            else:
                pass

        if self.verbose == 1:
            print(f"---- << SA layer >> ----")
            print("\n")

        return population
