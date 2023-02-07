
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Building_blocks.abc_Layer import Layer
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

        super().__init__()

        # -> Meta
        self.type = "MODEL"
        self.name = name

        self.verbose = verbose

        # -> Settings
        self.param = {
            # Model settings
            "evaluation_function": evaluation_function,
            "epochs": epochs,

            # Base weights
            "base_weights": {},
            "weight_curves": {},

            # Misc
            "optimisation_mode": optimisation_mode,
            "non_training_layers": ["RESET", "MODULATOR", "STEP", "MODEL"],
        }

        self.layers = layers

    def __str__(self):
        for layer in self.layers:
            if layer.type == "MODEL":
                print(f" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SUB-MODEL - {layer.param['epochs']} epochs")
                print(layer, end="")
                print(f" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
                print("_________________________________________________________________________________")

            else:
                print(f"{layer.ref} {layer}")
                if layer != self.layers[-1]:
                    print("_________________________________________________________________________________")

        return ""

    @property
    def layer_count(self):
        """ Returns the number of layers in the model"""
        return len(self.layers)

    @property
    def training_steps_count(self):
        """ Returns the number of training steps in the model"""
        return self.layer_count * self.epochs

    @staticmethod
    def count_training_layers(layer_list):
        """
        Counts the number of training layers in the model

        :param layer_list: list of layers
        :return: int of training layers count
        """

        training_layers_count = 0

        # -> Get dict of layer types and their respective count
        count_layer_types = self.count_layer_types(layer_list=layer_list)

        # -> Count training layers
        for layer_type in count_layer_types.keys():
            if layer_type not in self.param["non_training_layers"]:
                training_layers_count += count_layer_types[layer_type]

        return training_layers_count

    def count_layer_types(self, layer_list: list, layer_types_dict=None):
        """
        Counts the number of layers of each type in the model

        :param layer_list: list of layers
        :param layer_types_dict: base dict of layer types and their count
        :return: dict of layer types and their count
        """

        if layer_types_dict is None:
            layer_types_dict = {}

        for layer in layer_list:
            if layer.type == "MODEL":
                layer_types_dict = self.count_layer_types(layer_list=layer.layers, layer_types_dict=layer_types_dict)

            else:
                if layer.type not in layer_types_dict.keys():
                    layer_types_dict[layer.type] = 1
                else:
                    layer_types_dict[layer.type] += 1

        return layer_types_dict

    def summary(self):
        # -> Count step types
        layer_types_dict = self.count_layer_types(layer_list=self.layers)

        # --> Print model structure
        print("=================================================================================")
        print("|                                MODEL Structure                                |")
        print("=================================================================================")
        print(self.__str__())

        print("=================================================================================\n")
        print("-> Epoch training steps count:")
        for layer_type in layer_types_dict.keys():
            if layer_type not in self.param["non_training_layers"]:
                print(f" - {layer_type} steps: {layer_types_dict[layer_type]}")

        print("\n-> Cumulated training steps count:")

        # --> Print run recap
        for layer_type in layer_types_dict.keys():
            if layer_type not in self.param["non_training_layers"]:
                print(f" - {layer_type} steps: {layer_types_dict[layer_type] * self.param['epochs']}")

        print("\n=================================================================================\n")

        return

    def add_layer(self, layer):
        self.layers.append(layer)

    def step(self, population, evaluation_function, optimisation_mode: str, epoch, data=None, settings=None):
        """
        Perform a round of the model training

        :param population: Population object
        :param evaluation_function: Function to evaluate individuals
        :param optimisation_mode: min or max
        :param epoch: Current epoch
        :param data: Data to evaluate individuals on
        :param settings: Settings to use for evaluation

        :return: Population object
        """
        self.evaluation_function = evaluation_function

        return self.train(population, data=data, settings=settings)

    def train(self, population, data=None, settings=None):
        if self.verbose == 1:
            self.summary()

        # -> Define training variables (adjustable using modulator layers)
        evaluation_function = self.param["evaluation_function"]
        optimisation_mode = self.param["optimisation_mode"]
        data = data
        settings = settings

        # -> Prime layers
        for layer in self.layers:
            layer.prime(epochs=self.param["epochs"])

        # ----- Perform training
        for epoch in range(self.param["epochs"]):
            if self.verbose == 1:
                print(f"============================================= Epoch {epoch + 1}")

            # -> Process all layers
            for layer in self.layers:
                # -> Process modulator layer
                if layer.type == "MODULATOR":
                    evaluation_function = layer.step(evaluation_function=evaluation_function,
                                                     epoch=epoch,
                                                     data=data,
                                                     settings=settings)

                # -> Process all other layers
                else:
                    population = layer.step(population=population,
                                            evaluation_function=evaluation_function,
                                            optimisation_mode=optimisation_mode,
                                            epoch=epoch,
                                            data=data,
                                            settings=settings)

        # ----- Summaries training results
        if self.verbose == 1:
            print("")
            print("Training complete")
            print("--------------------------------------------------------------------------------------")

            # --> Evaluate population
            fitness_evaluation = population.get_fitness_evaluation(evaluation_function=evaluation_function,
                                                                   data=data,
                                                                   settings=settings,
                                                                   optimisation_mode=optimisation_mode)

            print("")
            print("Best solution fitness:", population.best_fitness_history[-1])

            print("Population avg fitness:", round(sum(fitness_evaluation)/len(fitness_evaluation), 2))
            print(f"Population avg age: "
                  f"{sum(population.get_individual_ages())/len(population.get_individual_ages())} epochs")

        return population
