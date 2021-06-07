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


class Individual(ABC):
    def __init__(self):

        self.fitness_history = []

        self.parameter_set = None

        return

    @abstractmethod
    def gen_parameter_set(self):
        return
