
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys
from math import log10

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2021'

##################################################################################################################


def throttle(current_iteration, nb_of_iterations, max_value, min_value=1., decay_function=0):
    """
    Throttle a value according to the instance in the run time.

    The following decay functions settings can be used:
            0 - Fixed value (returns max value)

            1 - Linear decay

            2 - Logarithmic decay (in development)

    :param current_iteration: Current iteration
    :param nb_of_iterations: Total number of iteration to consider
    :param max_value: Max allowed value
    :param min_value: Min allowed value
    :param decay_function: Decay function setting
    :return: Throttled value
    """

    inverse = False
    if max_value < min_value:
        inverse = True

    # TODO: add decay functions (log/exponential etc...)
    if current_iteration <= nb_of_iterations:
        # --> Fixed value decay
        if decay_function == 0:
            return max_value

        # --> Linear decay
        elif decay_function == 1:
            if inverse:
                throttled_value = max_value + (min_value - max_value) / nb_of_iterations * current_iteration

                if throttled_value <= min_value:
                    throttled_value = min_value
            else:
                throttled_value = max_value - (max_value - min_value) / nb_of_iterations * current_iteration

                if throttled_value <= min_value:
                    throttled_value = min_value

        # --> Logarithmic decay
        # TODO: Complete log decay
        elif decay_function == 2:
            throttled_value = max_value + log10(-(current_iteration - nb_of_iterations))

        # --> Exit program if incorrect settings used
        else:
            sys.exit("Invalid throttle decay function reference")

    else:
        throttled_value = min_value

    return throttled_value
