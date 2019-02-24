from PIL import Image
from geometry import *

n_individuals = 21      # Number of individuals (From 1 to inf, elitism + n_individuals must be pair)
n_polygons = 100        # Number of polygons each individual starts with (From 1 to inf)
n_vertices = 4          # Number of vertices for each individual (From 3 to inf)
reference_image = Image.open('../data/97px-monalisa.jpg')

# Initialize population with previous parameters.
population = Population(n_individuals, n_polygons, n_vertices, reference_image)

generations = 1000000   # Number of generations to evolve the population (From 1 to inf)
tournament_size = 5     # Tournament size for crossover selection (From 1 to n_individuals)
p_crossover = 0.05      # Probability that two polygons are swapped during crossover (From 0 to 0.5)
sigma_color = 1         # Stregth of the mutation (From 0 to inf, although it is recomented to be < 1)
sigma_shape = 1         # Stregth of the mutation (From 0 to inf, although it is recomented to be < 1)
p_relative = 0.3
elitism = 1             # Individuals passed to next generation by elitism (From 0 to n_individuals)
results_path = '../results/geneticalgorithm'

# Start the evolution with previous parameters
population.evolution(generations, tournament_size, p_crossover,
                     sigma_color, sigma_shape, p_relative,
                     elitism, results_path)