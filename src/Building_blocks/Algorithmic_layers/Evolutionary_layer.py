
################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys

# Own modules
from src.Building_blocks.abc_Layer import Layer
from src.Building_blocks.Population import Population
from src.Tools.Parameter_tools import *

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################

ELITIC = 0

SELECTION_METHODS = ["ELITIC"]


class EVO_layer(Layer):
    def __init__(self,
                 # EVO settings
                 parameter_randomiser,
                 individual_template,
                 selection_method: int = ELITIC,
                 parameters_decay_function: int = 0,

                 # Weights
                 percent_parents: int or float or list = 0.3,
                 percent_parents_in_next_gen: int or float or list = 0.1,
                 percent_random_ind_in_next_gen: int or float or list = 0.1,
                 mutation_rate: int or float or list = 0.2,

                 parameters_throttle_curves: dict or None = None,

                 # Blacklisted parameters
                 parameter_blacklist: list = [],

                 # Misc settings
                 optimisation_mode: str = None,
                 evaluation_function=None,
                 verbose=0,
                 name="Layer"):
        """
        Initialise an EVO layer.

        selection_method:
            0: Elitic selection

        :param parameter_randomiser:
        :param individual_template:
        :param selection_method:
        :param parameters_decay_function:
        :param percent_parents:
        :param percent_parents_in_next_gen:
        :param percent_random_ind_in_next_gen:
        :param mutation_rate:
        :param parameters_throttle_curves: A dict of throttle curves for each parameter,
                                           each curve is a list of at least 2 values
        :param parameter_blacklist:
        :param optimisation_mode: min or max
        :param evaluation_function:
        :param verbose:
        :param name:
        """

        super().__init__(name=name, verbose=verbose)

        # -> Meta
        self.type = "EVO"

        # -> Settings
        self.param = {
            # EVO settings
            "parameter_randomiser": parameter_randomiser,
            "individual_template": individual_template,
            "selection_method": selection_method,
            "parameters_decay_function": parameters_decay_function,

            "parameters_throttle_curves": parameters_throttle_curves,
            "parameters_throttle_curves_scaled": {},

            # Weight curves
            "weight_curves": {
                "percent_parents": {
                    "reference_curve": percent_parents if type(percent_parents) is list
                                        else [percent_parents, percent_parents],
                    "scaled_curve": None,
                },

                "percent_parents_in_next_gen": {
                    "reference_curve": percent_parents_in_next_gen if isinstance(percent_parents_in_next_gen, list)
                                        else [percent_parents_in_next_gen, percent_parents_in_next_gen],
                    "scaled_curve": None,
                },

                "percent_random_ind_in_next_gen": {
                    "reference_curve": percent_random_ind_in_next_gen if isinstance(percent_random_ind_in_next_gen, list)
                                        else [percent_random_ind_in_next_gen, percent_random_ind_in_next_gen],
                    "scaled_curve": None,
                },

                "mutation_rate": {
                    "reference_curve": mutation_rate if isinstance(mutation_rate, list)
                                        else [mutation_rate, mutation_rate],
                    "scaled_curve": None,
                },
            },

            # Blacklist
            "parameter_blacklist": parameter_blacklist,

            # Misc
            "optimisation_mode": optimisation_mode,
            "evaluation_function": evaluation_function,
        }

    def __str__(self):
        """
        :return: String representation of layer
        """

        # -> Construct layer info
        layer_info = f"> {self.name} - Evolutionary" + \
                     f"\n     - Selection method: {SELECTION_METHODS[self.param['selection_method']]} \n"
        layer_info += self.weights_summary()

        return layer_info

    def step(self, population, evaluation_function, optimisation_mode: str, epoch: int, data=None, settings=None):
        """
        Perform a single step of the EVO layer.

        :param population: Population object
        :param evaluation_function: Function to evaluate individuals
        :param optimisation_mode: min or max
        :param epoch: Current epoch
        :param data: Data to evaluate individuals on
        :param settings: Settings to pass to the layer

        :return: Population object
        """

        # -> Get epoch weights
        epoch_weights = self.get_epoch_weights(epoch=epoch)

        # ============================================================== Evaluate population
        # !!! Properties set in layer are always prioritised over properties provided by model !!!
        if self.param["evaluation_function"] is not None:
            evaluation_function = self.param["evaluation_function"]

        if self.param["optimisation_mode"] is not None:
            optimisation_mode = self.param["optimisation_mode"]

        fitness_evaluation = population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                                               data=data,
                                                               settings=settings,
                                                               optimisation_mode=optimisation_mode)

        # ============================================================== Prepare next generation
        parents_count = round(len(population) * epoch_weights['percent_parents'])
        parents_count_in_next_gen = round(len(population) * epoch_weights['percent_parents_in_next_gen'])
        random_ind_count_in_next_gen = round(len(population) * epoch_weights['percent_random_ind_in_next_gen'])

        assert len(population) >= parents_count_in_next_gen + random_ind_count_in_next_gen, \
            "!!! Sum of desired parent count and random individual count larger than total population size !!!"

        # ============================================================== Select parents
        parents = []

        # --> Select individuals
        # TODO: Implement alternative selection methods

        # Elitic selection
        if self.param['selection_method'] == ELITIC:
            # Use bubblesort to sort population and fitness_evaluation according to fitness_evaluation
            for _ in range(len(fitness_evaluation)):
                for i in range(len(fitness_evaluation) - 1):
                    if optimisation_mode == "max":         # -> Sorting from large to small
                        if fitness_evaluation[i] < fitness_evaluation[i + 1]:
                            # Reorder population
                            population[i], population[i + 1] = population[i + 1], population[i]

                            # Reorder fitness evaluation
                            fitness_evaluation[i], fitness_evaluation[i + 1] = fitness_evaluation[i + 1], fitness_evaluation[i]

                    elif optimisation_mode == "min":       # -> Sorting from small to large
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

        # ============================================================== Generate new population
        adjustable_parameter_count = \
            parents[0].get_adjustable_parameter_count(layer_parameter_blacklist=self.param['parameter_blacklist'])

        nb_of_parameters_to_mutate = round(adjustable_parameter_count * epoch_weights['mutation_rate']) or 1

        # --> Add required number of parents to new population (from best to worst)
        new_population = Population()
        new_population += population[:parents_count_in_next_gen]

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
                parameter_to_modify = select_random_parameter_to_modify(individual=offspring,
                                                                        layer_parameter_blacklist=self.param['parameter_blacklist'])

                # Modify parameter
                offspring.parameter_set = \
                    self.param['parameter_randomiser'](parameter_set=offspring.parameter_set,
                                                       parameter_to_modify=parameter_to_modify,
                                                       current_epoch=epoch,
                                                       parameters_throttle_curves=self.param['parameters_throttle_curves_scaled'])

            # Add offspring to new population
            new_population.append(offspring)

        # --> Create random_ind number of random individuals and add to new population
        for _ in range(random_ind_count_in_next_gen):
            new_population.append(deepcopy(self.param['individual_template']()))

        # ============================================================== Print step info
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
