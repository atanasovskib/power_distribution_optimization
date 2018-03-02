from random import randint

from pyevolve import Consts, Util
from pyevolve.GenomeBase import GenomeBase


class ProposedDistributionGenome(GenomeBase):
    def __init__(self, num_populated_areas, num_power_plants):
        GenomeBase.__init__(self)
        self.proposed_distribution = None
        self.num_populated_areas = num_populated_areas
        self.num_power_plants = num_power_plants
        self.initializator.set(proposed_distribution_initializator)
        self.mutator.set(proposed_distribution_mutator)
        self.crossover.set(proposed_distribution_crossover)

    def copy(self, g):
        GenomeBase.copy(self, g)
        g.num_populated_areas = self.num_populated_areas
        g.num_power_plants = self.num_power_plants
        if self.proposed_distribution is not None:
            g.proposed_distribution = clone_matrix(self.proposed_distribution)

    def clone(self):
        new_copy = ProposedDistributionGenome(self.num_populated_areas, self.num_power_plants)
        self.copy(new_copy)
        return new_copy


def clone_matrix(matrix):
    to_return = []
    for row in matrix:
        to_return.append(row[:])

    return to_return


def proposed_distribution_initializator(genome, **args):
    if not isinstance(genome, ProposedDistributionGenome):
        raise ValueError(
            "proposed_distribution_initializator can only be used with genomes of type ProposedDistributionGenome")

    items = []
    for i in xrange(genome.num_populated_areas):
        items.append([])
        for j in xrange(genome.num_power_plants):
            random_gene = randint(0, 100)
            items[i].append(random_gene)

    genome.proposed_distribution = items


def proposed_distribution_mutator(genome, **args):
    if not isinstance(genome, ProposedDistributionGenome):
        raise ValueError("this mutator can only work with genomes of type ProposedDistributionGenome")

    if args["pmut"] <= 0.0:
        return 0

    height, width = genome.num_populated_areas, genome.num_power_plants
    elements = height * width

    mutations = args["pmut"] * elements

    range_min = 0
    range_max = 100

    if mutations < 1.0:
        mutations = 0
        for i in xrange(height):
            for j in xrange(width):
                if Util.randomFlipCoin(args["pmut"]):
                    random_int = randint(range_min, range_max)
                    genome.proposed_distribution[i][j] = random_int
                    mutations += 1

    else:
        for it in xrange(int(round(mutations))):
            which_x = randint(0, width - 1)
            which_y = randint(0, height - 1)
            random_int = randint(range_min, range_max)
            genome.proposed_distribution[which_y][which_x] = random_int

    return int(mutations)


def proposed_distribution_crossover(genome, **args):
    g_mom = args["mom"]
    g_dad = args["dad"]

    if not isinstance(g_mom, ProposedDistributionGenome):
        raise ValueError("this crossover is for ProposedDistributionGenome")

    if not isinstance(g_dad, ProposedDistributionGenome):
        raise ValueError("this crossover is for ProposedDistributionGenome")

    mom_clone = g_mom.clone()
    dad_clone = g_dad.clone()
    mom_clone.resetStats()
    dad_clone.resetStats()

    # print "Crossover old: ", mom_clone.proposed_distribution, ", ", dad_clone.proposed_distribution
    h, w = g_mom.num_populated_areas, g_mom.num_power_plants

    for i in xrange(h):
        for j in xrange(w):
            if Util.randomFlipCoin(Consts.CDefG2DBinaryStringUniformProb):
                temp = mom_clone.proposed_distribution[i][j]
                mom_clone.proposed_distribution[i][j] = dad_clone.proposed_distribution[i][j]
                dad_clone.proposed_distribution[i][j] = temp

    # print "Crossover new: ", mom_clone.proposed_distribution, ", ", dad_clone.proposed_distribution

    return mom_clone, dad_clone
