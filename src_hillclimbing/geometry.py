import math
import numpy as np
import random
from myrandom import randmut, int_truncated_gauss
from PIL import Image, ImageDraw
import copy

LEDGE = 10

class Polygon:

    __slots__ = 'vertices', 'color', 'xlim', 'ylim'

    def __init__(self, n_vertices, xlim, ylim):
        self.xlim = xlim
        self.ylim = ylim
        self.vertices = [tuple(random.randint(0-LEDGE, lim+LEDGE)
                               for lim in [xlim, ylim]) for _ in range(n_vertices)]
        self.color = tuple(random.randint(0, 255) for _ in ['r', 'g', 'b', 'a'])

    def mutate_color(self, sigma):
        s = sigma * 255

        idx = random.randint(0, 3)
        self.color = tuple(randmut(c, s, [0, 255])
                           if i == idx else c
                           for i, c in enumerate(self.color))

    def mutate_shape(self, sigma):
        sx, sy = sigma * self.xlim, sigma * self.ylim

        idx = random.randint(0, len(self.vertices) - 1)
        self.vertices = [(randmut(v[0], sx, [0-LEDGE, self.xlim+LEDGE]),
                          randmut(v[1], sy, [0-LEDGE, self.ylim+LEDGE]))
                         if i == idx else v
                         for i, v in enumerate(self.vertices)]

class Individual:

    __slots__ = 'polygons', 'n_vertices', 'xlim', 'ylim'

    def __init__(self, n_polygons, n_vertices, xlim, ylim):
        self.xlim = xlim
        self.ylim = ylim
        self.n_vertices = n_vertices
        self.polygons = [Polygon(n_vertices, xlim, ylim) for _ in range(n_polygons)]

    def fitness(self, reference_image):
        own_img = self.draw()
        ref_img = reference_image

        step = 1
        fitness = 0
        for i in range(0, self.xlim, step):
            for j in range(0, self.ylim, step):
                r_own, g_own, b_own = own_img.getpixel((i, j))
                r_ref, g_ref, b_ref = ref_img.getpixel((i, j))

                delta_r, delta_g, delta_b = r_ref - r_own, g_ref - g_own, b_ref - b_own

                color_difference = (delta_r * delta_r + delta_g * delta_g + delta_b * delta_b)

                fitness += color_difference

        return 1 - fitness / (3 * self.xlim/step * self.ylim/step * 255 * 255)

    def draw(self):
        background = Image.new('RGB', (self.xlim, self.ylim))
        drawing = ImageDraw.Draw(background, 'RGBA')

        for polygon in self.polygons:
            drawing.polygon(polygon.vertices, polygon.color)
        del drawing

        return background

class Population:

    __slots__ = 'xlim', 'ylim', 'reference_image', 'n_individuals', 'individuals'

    def __init__(self, n_individuals, n_polygons, n_vertices, reference_image):
        self.xlim, self.ylim = reference_image.size
        self.reference_image = reference_image
        self.n_individuals = n_individuals
        self.individuals = [Individual(n_polygons, n_vertices, self.xlim, self.ylim) for _ in range(n_individuals)]

    def evolution(self, generations,
                  sigma_color, sigma_shape, p_relative,
                  results_path):

        results = open(results_path + '/results.csv', 'w')
        results.write('generation,avg_fitness,best_fitness,worst_fitness,n_polygons,h')

        print('\nStarting evolution over {0} generations'.format(generations))

        fitness = [individual.fitness(self.reference_image) for individual in self.individuals]
        sc = sigma_color
        for generation in range(generations):
            # Results
            avg_fitness = sum(fitness) / len(fitness)
            best_fitness = max(fitness)
            worst_fitness = min(fitness)
            best_individual = self.individuals[fitness.index(best_fitness)]
            n_polygons = len(best_individual.polygons)

            results.write('\n{0},{1},{2},{3},{4}'.format(generation,avg_fitness,
                                                         best_fitness,worst_fitness,n_polygons))

            if generation % 1000 == 0:
                best_individual_drawing = best_individual.draw()
                best_individual_drawing.save(results_path + '/mona_lisa_{0}.png'.format(generation), 'PNG')

                print('\nGeneration {0} / {1}:'.format(generation, generations))
                print('\t- Average fitness: {0}'.format(avg_fitness))
                print('\t- Best fitness: {0}'.format(best_fitness))
                print('\t- Worst fitness: {0}'.format(worst_fitness))
                print('\t- Num polygons: {0}'.format(n_polygons))
                print('\t- Sigma: {0}'.format(sc))

            # Mutation
            sc = sigma_color * (1-avg_fitness)**0.25
            ss = sigma_shape * (1-avg_fitness)**0.25
            for i, individual in enumerate(self.individuals[elitism:], elitism):
                old = copy.deepcopy(individual)

                r = random.random()
                if r < p_relative:
                    polygon = np.random.choice(individual.polygons)
                    polygon.mutate_color(sc)
                else:
                    polygon = np.random.choice(individual.polygons)
                    polygon.mutate_shape(ss)

                f = individual.fitness(self.reference_image)
                if f > fitness[i]:
                    fitness[i] = f
                else:
                    self.individuals[i] = old

        print('\nEvolution completed!')
        results.close()