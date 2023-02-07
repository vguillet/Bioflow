
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################

class Population(list):
    def __init__(self):
        super().__init__()

        self.best_fitness_history = []
        self.best_individual_history = []

    def get_fitness_evaluation(self,
                               evaluation_function,
                               data,
                               settings,
                               optimisation_mode="max"):
        """
        Used to determine the fitness of all the individuals in a population.

        Note: When used, get_fitness_evaluation also stores the fitness of each individual in the
        respective individual's history

       :param evaluation_function: Function to evaluate individuals
        :param data: Data to evaluate individuals on
        :param settings: Settings to pass to the layer
        :param optimisation_mode: min or max

        :return: List of fitness values
        """
        fitness_evaluation = []

        for individual in self:
            # --> Evaluate individuals
            individual_fitness = individual.get_fitness_evaluation(
                evaluation_function=evaluation_function,
                data=data,
                settings=settings,
                record_evaluation=True
            )

            # --> Record individual fitness
            fitness_evaluation.append(individual_fitness)

            # --> Record solution if best overall
            if optimisation_mode == "max":  # -> Sorting from large to small
                if len(self.best_fitness_history) == 0 or individual_fitness > self.best_fitness_history[-1]:
                    self.best_fitness_history.append(individual_fitness)
                    self.best_individual_history.append(individual)

            elif optimisation_mode == "min":  # -> Sorting from large to small
                if len(self.best_fitness_history) == 0 or individual_fitness < self.best_fitness_history[-1]:
                    self.best_fitness_history.append(individual_fitness)
                    self.best_individual_history.append(individual)

            else:
                print("!!! Invalid Optimisation mode selected !!!")

        return fitness_evaluation

    def get_individual_ages(self):
        population_age = []

        for individual in self:
            population_age.append(len(individual.fitness_history))

        return population_age
