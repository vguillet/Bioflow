
################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
import random

# Libs

# Own modules
from src.Building_blocks.Population import Population


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class Model:
    def __init__(self,
                 evaluation_function,
                 layers: list = [],
                 epochs: int = 10):

        self.evaluation_function = evaluation_function

        self.layers = layers
        self.epochs = epochs

        self.layer_count = 0

        return

    def __str__(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for layer in self.layers:
            print(layer.layer_ref, layer)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return ""

    def add_layer(self, layer):
        if layer.layer_type != "RESET_layer" and layer.layer_type != "MODULATOR_layer":
            self.layer_count += 1
            layer.layer_ref = self.layer_count
            self.layers.append(layer)

        else:
            self.layers.append(layer)

        return

    def train(self, population):
        print("\n")
        print("--------------------------------------------------------------------------------------")
        print(self.__str__())

        evaluation_function = self.evaluation_function
        population = Population(population)

        # ----- Perform training
        for epoch in range(self.epochs):
            print(f"============================================= Epoch {epoch + 1}")
            # --> Set trackers to default
            step_tracker = epoch
            max_step_tracker = self.epochs

            for layer in self.layers:
                # --> Process reset layer
                if layer.layer_type == "RESET_layer":
                    evaluation_function_bool, step_tracker_bool, max_step_tracker_bool = layer.step()

                    if evaluation_function_bool:
                        evaluation_function = self.evaluation_function

                    if step_tracker_bool:
                        step_tracker = epoch

                    if max_step_tracker_bool:
                        max_step_tracker = self.epochs

                # --> Process modulator layer
                elif layer.layer_type == "MODULATOR_layer":
                    population, evaluation_function, step_tracker, max_step_tracker = layer.step(population=population,
                                                                                                 evaluation_function=evaluation_function,
                                                                                                 epoch=step_tracker,
                                                                                                 max_epoch=max_step_tracker)

                # --> Process all other layer
                else:
                    population = layer.step(population=population,
                                            evaluation_function=evaluation_function,
                                            epoch=step_tracker,
                                            max_epoch=max_step_tracker)

        print("\n")
        print("Training complete")
        print("--------------------------------------------------------------------------------------")

        # --> Evaluate population
        fitness_evaluation = population.get_fitness_evaluation(evaluation_function)
        fitness_evaluation.sort(reverse=True)

        print("\n")
        print("Best solution fitness:", max(fitness_evaluation))
        print("Best solution fitness history:", population.best_fitness_history)

        print("Population fitness:", fitness_evaluation)
        print("Population age:", population.get_individual_ages())

        return population


if __name__ == "__main__":
    from src.Building_blocks.Layers.Reset_layer import RESET_layer
    from src.Building_blocks.Layers.Modulator_layer import MODULATOR_layer
    from src.Building_blocks.Layers.Evolutionary_layer import EVO_layer
    from src.Building_blocks.Layers.Particle_swarm_optimisation_layer import PSO_Layer

    from src.Random.Evaluation_function_1 import param_sum
    from src.Random.Individual_1 import Indvidual_1
    from src.Random.Parameter_randomiser_1 import Randomiser_1

    # --> Construct model
    my_model = Model(evaluation_function=param_sum,
                     layers=[],
                     epochs=100)

    my_model.add_layer(EVO_layer(individual_template=Indvidual_1,
                                 parameter_randomiser=Randomiser_1,
                                 percent_parents=0.3,
                                 percent_parents_in_next_gen=0.2,
                                 percent_random_ind_in_next_gen=0.3,
                                 verbose=1))

    # my_model.add_layer(PSO_Layer(parameter_randomiser=Randomiser_1,
    #                              inertia_weight=0.729,
    #                              cognitive_weight=1.49445,
    #                              social_weight=1.49445,
    #                              verbose=1))

    my_model.add_layer(MODULATOR_layer(new_evaluation_function=None,
                                       new_step=10,
                                       new_max_step=100,
                                       verbose=0))

    my_model.add_layer(RESET_layer(evaluation_function_bool=False,
                                   step_bool=True,
                                   max_step_bool=True,
                                   verbose=0))

    # --> Create solution population
    my_solutions = []
    for _ in range(10):
        my_solutions.append(Indvidual_1())

    # --> Optimise solutions
    my_solutions = my_model.train(my_solutions)
