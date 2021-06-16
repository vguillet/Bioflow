
##################################################################################################################
"""

"""

# Built-in/Generic Imports

# Own modules
from src.Building_blocks.Population_tools import gen_initial_population
from src.Building_blocks.Model import Model
from src.Building_blocks.Algorithmic_layers.Evolutionary_layer import EVO_layer
from src.Building_blocks.Algorithmic_layers.Particle_swarm_optimisation_layer import PSO_Layer

from Test_cases.Rastrigin.Rastrigin_Individual import Rastrigin_Indvidual
from Test_cases.Rastrigin.Rastrigin_function import Rastrigin_function
from Test_cases.Rastrigin.Rastrigin_Parameter_randomiser import Rastrigin_randomiser
from Test_cases.Rastrigin.Rastrigin_VISU_layer import Rastrigin_VISU_layer

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
                  epochs=20)

sub_model.add_layer(PSO_Layer(inertia_weight=0.729,
                              cognitive_weight=1.49445,
                              social_weight=1.49445,
                              verbose=0))

sub_model.add_layer(PSO_Layer(inertia_weight=0.729,
                              cognitive_weight=1.49445,
                              social_weight=1.49445,
                              verbose=0))

# ------------------ Main model
my_model = Model(evaluation_function=function,
                 optimisation_mode="min",
                 layers=[],
                 epochs=20,
                 verbose=1)

my_model.add_layer(EVO_layer(individual_template=individual_template,
                             parameter_randomiser=randomiser,
                             percent_parents=0.3,
                             percent_parents_in_next_gen=0.2,
                             percent_random_ind_in_next_gen=0.3,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))

my_model.add_layer(PSO_Layer(inertia_weight=0.729,
                             cognitive_weight=1.49445,
                             social_weight=1.49445,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))

# my_model.add_layer(sub_model)

my_model.add_layer(PSO_Layer(inertia_weight=0.729,
                             cognitive_weight=1.49445,
                             social_weight=1.49445,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))

my_model.add_layer(PSO_Layer(inertia_weight=0.729,
                             cognitive_weight=1.49445,
                             social_weight=1.49445,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))

my_model.add_layer(PSO_Layer(inertia_weight=0.729,
                             cognitive_weight=1.49445,
                             social_weight=1.49445,
                             verbose=0))

my_model.add_layer(Rastrigin_VISU_layer(plot_rate=1))

my_model.add_layer(PSO_Layer(inertia_weight=0.729,
                             cognitive_weight=1.49445,
                             social_weight=1.49445,
                             verbose=0))

# --> Create solution population
my_solutions = gen_initial_population(individual_template=individual_template,
                                      population_size=100)

# --> Optimise solutions
my_solutions = my_model.train(my_solutions)
