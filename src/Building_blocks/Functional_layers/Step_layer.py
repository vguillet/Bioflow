
################################################################################################################
"""
STEP layer base class, to be used as parent to build STEP layers
"""

# Built-in/Generic Imports

# Libs

# Own modules
from src.Building_blocks.abc_Layer import Layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class STEP_layer(Layer):
    def __init__(self,
                 verbose=0,
                 name=""):

        super().__init__(name=name, verbose=verbose)

        # --> Meta
        self.type = "STEP"

    def __str__(self):
        return f"#######################> {self.name} ({self.type})"
