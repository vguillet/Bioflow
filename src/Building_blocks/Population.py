
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
    best_fitness_history = []
    best_individual_history = []

    def get_fitness_evaluation(self,
                               evaluation_function,
                               data,
                               optimisation_mode="max"):
        """
        Used to determine the fitness of all the individuals in a population.

        Note: When used, get_fitness_evaluation also stores the fitness of each individual in the
        respective individual's history

        :param evaluation_function:
        :param data:
        :param optimisation_mode:
        :return:
        """
        fitness_evaluation = []

        for individual in self:
            # --> Evaluate individuals
            individual_fitness = individual.get_fitness_evaluation(evaluation_function=evaluation_function,
                                                                   data=data,
                                                                   record_evaluation=True)

            # --> Record to individual history
            individual.fitness_history.append(individual_fitness)
            individual.parameter_set_history.append(individual.parameter_set)
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
