from random import randint

from pyevolve import Consts, Util
from pyevolve.GenomeBase import GenomeBase


class ProposedDistributionGenomeV2(GenomeBase):
    def __init__(self, loss_network):
        GenomeBase.__init__(self)
        self.proposed_distribution = None
        self.loss_network = loss_network
        self.num_populated_areas = len(loss_network)
        self.num_power_plants = len(loss_network[0])
        self.initializator.set(proposed_distribution_initializator)
        self.mutator.set(proposed_distribution_mutator)
        self.crossover.set(proposed_distribution_crossover)

    def copy(self, g):
        GenomeBase.copy(self, g)
        g.num_populated_areas = self.num_populated_areas
        g.num_power_plants = self.num_power_plants
        g.loss_network = self.loss_network
        if self.proposed_distribution is not None:
            g.proposed_distribution = clone_matrix(self.proposed_distribution)

    def clone(self):
        new_copy = ProposedDistributionGenomeV2(self.loss_network)
        self.copy(new_copy)
        return new_copy


def clone_matrix(matrix):
    to_return = []
    for row in matrix:
        to_return.append(row[:])

    return to_return


def proposed_distribution_initializator(genome, **args):
    if not isinstance(genome, ProposedDistributionGenomeV2):
        raise ValueError(
            "proposed_distribution_initializator can only be used with genomes of type ProposedDistributionGenome")

    items = []
    remaining = [100 for _ in xrange(genome.num_power_plants)]
    for i in xrange(genome.num_populated_areas):
        items.append([])
        for j in xrange(genome.num_power_plants):
            if genome.loss_network[i][j] != 0:
                rand = randint(0, 100)
                while rand > remaining[j] and rand > 1:
                    rand = int(rand * 0.9)
                random_gene = rand
                remaining[j] -= rand
                if remaining[j] == 0:
                    remaining[j] = 0
            else:
                random_gene = 0

            items[i].append(random_gene)

    genome.proposed_distribution = items


def proposed_distribution_mutator(genome, **args):
    if not isinstance(genome, ProposedDistributionGenomeV2):
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
                if genome.loss_network[i][j] == 0:
                    continue

                if Util.randomFlipCoin(args["pmut"]):
                    random_int = randint(range_min, range_max)
                    genome.proposed_distribution[i][j] = random_int
                    mutations += 1

    else:
        for it in xrange(int(round(mutations))):
            which_x = randint(0, width - 1)
            which_y = randint(0, height - 1)
            if genome.loss_network[which_y][which_x] == 0:
                continue

            random_int = randint(range_min, range_max)
            genome.proposed_distribution[which_y][which_x] = random_int

    return int(mutations)


def proposed_distribution_crossover(genome, **args):
    g_mom = args["mom"]
    g_dad = args["dad"]

    if not isinstance(g_mom, ProposedDistributionGenomeV2):
        raise ValueError("this crossover is for ProposedDistributionGenomeV2")

    if not isinstance(g_dad, ProposedDistributionGenomeV2):
        raise ValueError("this crossover is for ProposedDistributionGenomeV2")

    mom_clone = g_mom.clone()
    dad_clone = g_dad.clone()
    mom_clone.resetStats()
    dad_clone.resetStats()

    h, w = g_mom.num_populated_areas, g_mom.num_power_plants

    for i in xrange(h):
        for j in xrange(w):
            if mom_clone.loss_network[i][j] == 0:
                mom_clone.proposed_distribution[i][j] = 0
                dad_clone.proposed_distribution[i][j] = 0
            if Util.randomFlipCoin(Consts.CDefG2DBinaryStringUniformProb):
                temp = mom_clone.proposed_distribution[i][j]
                mom_clone.proposed_distribution[i][j] = dad_clone.proposed_distribution[i][j]
                dad_clone.proposed_distribution[i][j] = temp

    # print "Crossover new: ", mom_clone.proposed_distribution, ", ", dad_clone.proposed_distribution

    return mom_clone, dad_clone
