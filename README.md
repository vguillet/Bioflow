# Bioflow

A modular framework inspired from deep learning frameworks and models, allowing for creating optimisation models containing various sequences of optimisations steps.
The following algorithm layers are implemented:

- Evolutionary layer
- Swarm intelligence layer

The following are currently being investigated or in the process of being implemented:
- Cyclic Coordinate Search
- Powell’s Method
- Hooke-Jeeves Method
- Nelder-Mead Simplex Search

- Simulated Annealing
- Cross-Entropy Method

- Genetic Algorithm
- Differential Evolution

The framework also contain a number of layers used to control various metaparameters during the optimisation process.

For a given problem, the following need to be created:
- Individual: class with parameter set attribute + parameter set generator function modifying  parameter set attribute(for evo layers)
- Parameter randomiser  (for evo layers): class with method (input: paramer_set dictionary, paramer_set dictionary with modified parameter set)
- Evaluation function: function computing fitness of individual (input: Individual, output fitness)
- Visualiser (optional)
