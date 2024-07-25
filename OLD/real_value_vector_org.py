import numpy as np
import random
from math import sqrt

LENGTH = None
RANGE_MIN = None
RANGE_MAX = None
MUTATION_EFFECT_SIZE = None

class RealValueVectorOrg(object):
    """
    this is a class that represents organisms as a real value array
    fitness is determined by calling the fitness fuction
    the length is determined at object creation
    """

    def __init__(self, genotype=None):
        if genotype is None:
            genotype = _create_random_genotype()
        else:
            genotype = np.asarray(genotype, dtype=np.float64)
        self.genotype = genotype
        self._fitness_cache = None

    def fitness(self, environment):
        if self._fitness_cache is None:
            self._fitness_cache = {}
            self._fitness_cache[environment] = environment(self.genotype)
        elif environment not in self._fitness_cache:
            self._fitness_cache[environment] = environment(self.genotype)
        return self._fitness_cache[environment]

    def reset_fitness_cache(self):
        self._fitness_cache = None

    def get_mutant(self):        
        return RealValueVectorOrg(_get_mutated_genotype(self.genotype, MUTATION_EFFECT_SIZE))

    def __eq__(self, other):
        return self.genotype == other.genotype

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "RealValueVectorOrg({})".format(self.genotype)

    def __repr__(self):
        return str(self)

    def is_better_than(self, other, environment):
        return self.fitness(environment) < other.fitness(environment)

    def distance(self, other, environment):
        dist = 0.0
        for i in range(self.genotype.shape[0]):
            dist += (self.genotype[i] - other.genotype[i])**2

        return sqrt(dist)

def _get_mutated_genotype(genotype, effect_size):
    """Mutates one locus in organism at random"""
    mut_location = random.randrange(genotype.shape[0])
    delta = random.normalvariate(0, effect_size)
    mutant_value = genotype[mut_location] + delta
    #Ensure a copy is made so mutant doesn't edit the original
    mutant = np.array(genotype, copy=True)
    mutant[mut_location] = _wrap_around(mutant_value, RANGE_MIN, RANGE_MAX)            
    return mutant

def _wrap_around(value, min_, max_):
    """Literally does what it says."""
    width = max_ - min_
    while value < min_ or value > max_:
        if value < min_:
            value += width
        else:
            value -= width
    return value

def _create_random_genotype():
    """Create a random array genotype"""
    genotype = np.zeros(LENGTH, dtype=np.float64)
    for i in range(LENGTH):
        genotype[i] = random.uniform(RANGE_MIN, RANGE_MAX)
    return genotype
