from pyevolve import GSimpleGA, Consts

from distribution_grid import DistributionGrid
from populated_area import PopulatedArea
from power_plant import PowerPlant
from proposed_distribution_genome import ProposedDistributionGenome
from test_examples.TestExample2c import TestExample2c

populated_areas = []
power_plants = []
distribution_grid = None


def num_errors_for_electricity_given_where_no_grid(proposed_distribution, num_populated_areas, num_power_plants):
    num_errors = 0
    for i in xrange(num_populated_areas):
        for j in xrange(num_power_plants):
            if proposed_distribution[i][j] > 0 and distribution_grid.losses[i][j] == 0:
                num_errors += proposed_distribution[i][j]

    return num_errors


def num_plants_over_capacity(proposed_distribution, num_populated_areas, num_power_plants):
    num_errors = 0
    for j in xrange(num_power_plants):
        allocated_capacity = 0
        for i in xrange(num_populated_areas):
            allocated_capacity += proposed_distribution[i][j]
        if allocated_capacity > 100:
            num_errors += (allocated_capacity - 100)

    return num_errors


def num_areas_with_not_enough_energy(proposed_distribution, num_populated_areas, num_power_plants):
    num_errors = 0
    # print "Yo dawg"
    for i in xrange(num_populated_areas):
        effective_power = 0.0
        # print "Place: ", i
        for j in xrange(num_power_plants):
            produced_power_at_plan = power_plants[j].production_at_max_capacity * (proposed_distribution[i][j] / 100.0)
            # print "Plant: ", j, " produced power: ", produced_power_at_plan
            loss_coefficient = 0
            if distribution_grid.losses[i][j] != 0:
                loss_coefficient = (100 - distribution_grid.losses[i][j]) / 100.0
            effective_power += produced_power_at_plan * loss_coefficient
        # print "Effective power: ", effective_power, "reqiured: ", populated_areas[i].consumed_electricity
        if effective_power < populated_areas[i].consumed_electricity:
            diff = populated_areas[i].consumed_electricity - effective_power
            if diff < 1:
                diff = 1
            num_errors += diff

    return num_errors


def eval_function(chromosome, print_to_console=False):
    if not isinstance(chromosome, ProposedDistributionGenome):
        raise ValueError("this eval function can only work with ProposedDistributionGenome")

    # penalty for giving electricity where a plant is not supposed to = 100 * calculated_price
    # penalty for giving more electricity than a plant can produce = 100 * calculated_price
    # penalty for given electricity is not  enough for populated area = 10 * calculated_price
    price = 0.0
    num_populated_areas = chromosome.num_populated_areas
    num_power_plants = chromosome.num_power_plants
    proposed_distribution = chromosome.proposed_distribution

    for j in xrange(num_power_plants):
        allocated_for_plant = 0
        for i in xrange(num_populated_areas):
            allocated_for_plant += proposed_distribution[i][j]
        price_for_plant = allocated_for_plant * power_plants[j].price_at_max_capacity / 100.0
        price += price_for_plant

    if print_to_console:
        print "Price without penalties: ", price
    most_expensive_plant = max(map(lambda x: x.price_at_max_capacity, power_plants))
    if price == 0:
        price = most_expensive_plant * num_power_plants

    num_errors_for_grid_violation = num_errors_for_electricity_given_where_no_grid(proposed_distribution,
                                                                                   num_populated_areas,
                                                                                   num_power_plants)
    if num_errors_for_grid_violation > 0:
        price *= (num_errors_for_grid_violation * most_expensive_plant)

    num_over_capacity = num_plants_over_capacity(proposed_distribution, num_populated_areas, num_power_plants)
    if num_over_capacity > 0:
        price *= (num_over_capacity * most_expensive_plant * 10)

    num_not_enough_energy = num_areas_with_not_enough_energy(proposed_distribution, num_populated_areas,
                                                             num_power_plants)

    if num_not_enough_energy > 0:
        price *= (num_not_enough_energy * most_expensive_plant * 10)

    if print_to_console:
        print "Chromo:", proposed_distribution
        print "Num over capacity: ", num_over_capacity, " Num grid violations", num_errors_for_grid_violation, \
            "Num areas not enough power:", num_not_enough_energy, " Calculated price: ", price
    return price


if __name__ == '__main__':
    test_example = TestExample2c()
    num_populated_areas = test_example.get_num_cities()
    num_power_plants = test_example.get_num_power_plants()
    reqs_pop = test_example.get_power_requirements()

    for i in xrange(num_populated_areas):
        populated_areas.append(PopulatedArea(reqs_pop[i]))

    power_plants = []
    for plant in xrange(num_power_plants):
        power_plants.append(PowerPlant(test_example.get_max_production_capacity()[plant], test_example.get_price_at_max_capacity()[plant]))

    #
    # print "Required amount of electricity: ", amm_req
    # print "Total possible amount: ", amm_gen
    losses = []
    # for i in xrange(num_populated_areas):
    #     losses.append([])
    #     for j in xrange(num_power_plants):
    #         losses[i].append(10)

    losses = test_example.get_loss_matrix()
    distribution_grid = DistributionGrid(losses)

    genome = ProposedDistributionGenome(num_populated_areas, num_power_plants)
    genome.evaluator.set(eval_function)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(10000)
    ga.setPopulationSize(1000)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(0.5)
    ga.setMutationRate(0.5)
    ga.setElitism(True)
    ga.setElitismReplacement(1)
    ga.evolve(freq_stats=500)
    print "--------------"
    print ga.bestIndividual().proposed_distribution
    print eval_function(ga.bestIndividual(), print_to_console=True)
