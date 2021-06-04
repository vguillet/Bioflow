################################################################################################################
"""

"""

# Built-in/Generic Imports
import json
import random
from abc import ABC, abstractmethod

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class Layer(ABC):
    def __init__(self):

        self.layer_type = None

        return

    @abstractmethod
    def __str__(self):
        return

    @abstractmethod
    def step(self, population, evaluation_function, epoch, max_epoch):
        return population
