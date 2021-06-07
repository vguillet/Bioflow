
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Building_blocks.Layers.abc_Layer import Layer
from src.Building_blocks.Population import Population


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class Model(Layer):
    def __init__(self,
                 evaluation_function,
                 optimisation_mode="max",
                 layers: list = [],
                 epochs: int = 10,
                 verbose=0,
                 name="Model"):
        # --> Meta
        self.ref = ""
        self.type = "MODEL"
        self.name = name

        self.verbose = verbose
        self.optimisation_mode = optimisation_mode

        # --> Settings
        self.evaluation_function = evaluation_function

        self.layers = layers
        self.epochs = epochs

        self.layer_count = 0

        return

    def __str__(self):
        for layer in self.layers:
            if layer.type == "MODEL":
                print(f"  >>>>>>>> SUB-MODEL - {layer.epochs} epochs")
                print(layer, end="")
                print("  >>>>>>>>")

            else:
                print(f"  {layer.ref} {layer}")

        return ""

    def summary(self):
        # --> Count step types
        def count_layer_types(layer_list, layers_count):
            for layer in layer_list:
                if layer.type == "MODEL":
                    count_layer_types(layer.layers, layers_count)

                else:
                    if layer.type in layers_count.keys():
                        layers_count[layer.type] += 1
                    else:
                        layers_count[layer.type] = 1

            return layers_count

        layers_counter = count_layer_types(layer_list=self.layers,
                                           layers_count={})

        # --> Print model structure
        print("=================================================================================")
        print("                                 MODEL Structure                                 ")
        print("=================================================================================")
        print("")
        print(self.__str__())
        print("=======================================")

        print("")
        print("-> Epoch training steps count:")
        for key in layers_counter.keys():
            if key != "RESET" and key != "MODULATOR" and key != "STEP" and key != "MODEL":
                print(f" - {key} steps: {layers_counter[key]}")

        print("")
        print("-> Full training steps count:")

        # --> Print run recap
        for key in layers_counter.keys():
            if key != "RESET" and key != "MODULATOR" and key != "STEP" and key != "MODEL":
                print(f" - {key} steps: {layers_counter[key] * self.epochs}")

        print("")
        print("=================================================================================\n")

        return

    def add_layer(self, layer):
        if layer.type != "RESET" and layer.type != "MODULATOR" and layer.type != "STEP":
            # --> Set layer ref
            self.layer_count += 1
            layer.ref = self.layer_count

            # --> Set optimisation mode
            layer.optimisation_mode = self.optimisation_mode

            self.layers.append(layer)

        else:
            self.layers.append(layer)

        return

    def step(self, population, evaluation_function, epoch, max_epoch, data=None):
        self.evaluation_function = evaluation_function

        return self.train(population, data=data)

    def train(self, population, data=None):
        if self.verbose == 1:
            print("\n")
            print("--------------------------------------------------------------------------------------")
            self.summary()

        evaluation_function = self.evaluation_function
        population = Population(population)

        # ----- Perform training
        for epoch in range(self.epochs):
            if self.verbose == 1:
                print(f"============================================= Epoch {epoch + 1}")

            # --> Set trackers to default
            step_tracker = epoch
            max_step_tracker = self.epochs

            for layer in self.layers:
                # --> Process reset layer
                if layer.type == "RESET":
                    evaluation_function_bool, step_tracker_bool, max_step_tracker_bool = layer.step()

                    if evaluation_function_bool:
                        evaluation_function = self.evaluation_function

                    if step_tracker_bool:
                        step_tracker = epoch

                    if max_step_tracker_bool:
                        max_step_tracker = self.epochs

                # --> Process modulator layer
                elif layer.type == "MODULATOR":
                    population, evaluation_function, step_tracker, max_step_tracker = layer.step(population=population,
                                                                                                 evaluation_function=evaluation_function,
                                                                                                 epoch=step_tracker,
                                                                                                 max_epoch=max_step_tracker)

                # --> Process all other layer
                else:
                    population = layer.step(population=population,
                                            evaluation_function=evaluation_function,
                                            epoch=step_tracker,
                                            max_epoch=max_step_tracker,
                                            data=data)

        # ----- Summaries training results
        if self.verbose == 1:
            print("")
            print("Training complete")
            print("--------------------------------------------------------------------------------------")

            # --> Evaluate population
            fitness_evaluation = population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                                                   data=data,
                                                                   optimisation_mode=self.optimisation_mode)

            print("")
            print("Best solution fitness:", population.best_fitness_history[-1])

            print("Population avg fitness:", round(sum(fitness_evaluation)/len(fitness_evaluation), 2))
            print(f"Population avg age: "
                  f"{sum(population.get_individual_ages())/len(population.get_individual_ages())} epochs")

        return population
