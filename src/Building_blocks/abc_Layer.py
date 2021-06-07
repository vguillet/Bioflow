
################################################################################################################
"""
Ensure that the new population is an edited version of the old one
or the new population is a Population class instance
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
    @abstractmethod
    def __init__(self):
        return

    @abstractmethod
    def __str__(self):
        return

    @abstractmethod
    def step(self, population, evaluation_function, epoch, max_epoch, data=None, settings=None):
        return population
