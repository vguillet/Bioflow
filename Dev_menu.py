
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import json

# Own modules
from src.Building_blocks.Model import Model
from src.Building_blocks.Layers.Evolutionary_layer import EVO_layer
from src.Building_blocks.Layers.Particle_swarm_optimisation_layer import PSO_Layer

from src.Random.Rastrigin.Rastrigin_Individual import Rastrigin_Indvidual
from src.Random.Rastrigin.Rastrigin_function import Rastrigin_function
from src.Random.Rastrigin.Rastrigin_Parameter_randomiser import Rastrigin_randomiser
from src.Random.Rastrigin.Rastrigin_VISU_layer import Rastrigin_VISU_layer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################

individual_template = Rastrigin_Indvidual
randomiser = Rastrigin_randomiser
function = Rastrigin_function

# --> Construct model
sub_model = Model(evaluation_function=function,
                  optimisation_mode="min",
                  layers=[],
                  epochs=10)

sub_model.add_layer(PSO_Layer(parameter_randomiser=randomiser,
                              inertia_weight=0.729,
                              cognitive_weight=1.49445,
                              social_weight=1.49445,
                              verbose=0))

sub_model.add_layer(PSO_Layer(parameter_randomiser=randomiser,
                              inertia_weight=0.729,
                              cognitive_weight=1.49445,
                              social_weight=1.49445,
                              verbose=0))

# ------------------ Main model
my_model = Model(evaluation_function=function,
                 optimisation_mode="min",
                 layers=[],
                 epochs=10,
                 verbose=1)

my_model.add_layer(EVO_layer(individual_template=individual_template,
                             parameter_randomiser=randomiser,
                             percent_parents=0.3,
                             percent_parents_in_next_gen=0.2,
                             percent_random_ind_in_next_gen=0.3,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))

my_model.add_layer(PSO_Layer(parameter_randomiser=randomiser,
                             inertia_weight=0.729,
                             cognitive_weight=1.49445,
                             social_weight=1.49445,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))

# my_model.add_layer(sub_model)

my_model.add_layer(PSO_Layer(parameter_randomiser=randomiser,
                             inertia_weight=0.729,
                             cognitive_weight=1.49445,
                             social_weight=1.49445,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))


# --> Create solution population
my_solutions = []
for _ in range(100):
    my_solutions.append(individual_template())

# --> Optimise solutions
my_solutions = my_model.train(my_solutions)
