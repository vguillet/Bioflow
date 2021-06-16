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


class Model(ABC):
    def __init__(self):
        self.layer_dict = {}
        return

    @abstractmethod
    def init_parameters(self):
        return

    @abstractmethod
    def step(self):
        return
