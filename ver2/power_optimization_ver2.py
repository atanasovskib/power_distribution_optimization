from pyevolve import GSimpleGA, Consts

from populated_area import PopulatedArea
from power_plant import PowerPlant
from proposed_distribution_genome_v2 import ProposedDistributionGenomeV2
from test_examples.TestExample import TestExample
from test_examples.TestExample1a import TestExample1a
from test_examples.TestExample1b import TestExample1b
from test_examples.TestExample1c import TestExample1c
from test_examples.TestExample2a import TestExample2a
from test_examples.TestExample2b import TestExample2b
from test_examples.TestExample2c import TestExample2c
from test_examples.TestExample3a import TestExample3a
from ver2.GAProperties import GAProperties


def num_errors_for_electricity_given_where_no_grid(proposed_distribution, num_populated_areas,
                                                   num_power_plants, losses):
    num_errors = 0
    for i in xrange(num_populated_areas):
        for j in xrange(num_power_plants):
            if proposed_distribution[i][j] > 0 and losses[i][j] == 0:
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


def num_areas_with_not_enough_energy(proposed_distribution, power_plants, losses, populated_areas, num_populated_areas,
                                     num_power_plants):
    num_errors = 0
    # print "Yo dawg"
    for i in xrange(num_populated_areas):
        effective_power = 0.0
        # print "Place: ", i
        for j in xrange(num_power_plants):
            produced_power_at_plan = power_plants[j].production_at_max_capacity * (proposed_distribution[i][j] / 100.0)
            # print "Plant: ", j, " produced power: ", produced_power_at_plan
            loss_coefficient = 0
            if losses[i][j] != 0:
                loss_coefficient = (100 - losses[i][j]) / 100.0
            effective_power += produced_power_at_plan * loss_coefficient
        # print "Effective power: ", effective_power, "reqiured: ", populated_areas[i].consumed_electricity
        if effective_power < populated_areas[i].consumed_electricity:
            diff = populated_areas[i].consumed_electricity - effective_power
            if diff < 1:
                diff = 1
            num_errors += diff

    return num_errors


def eval_function(chromosome, power_plants, losses, populated_areas, print_to_console=False):
    if not isinstance(chromosome, ProposedDistributionGenomeV2):
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
    if price < 1:
        price = most_expensive_plant * num_power_plants

    num_errors_for_grid_violation = num_errors_for_electricity_given_where_no_grid(proposed_distribution,
                                                                                   num_populated_areas,
                                                                                   num_power_plants, losses)
    if num_errors_for_grid_violation > 0:
        if price < most_expensive_plant:
            price = most_expensive_plant
        price *= (num_errors_for_grid_violation + 1)

    num_over_capacity = num_plants_over_capacity(proposed_distribution, num_populated_areas, num_power_plants)
    if num_over_capacity > 0:
        if price < most_expensive_plant:
            price = most_expensive_plant
        price *= (num_over_capacity + 1)

    num_not_enough_energy = num_areas_with_not_enough_energy(proposed_distribution,
                                                             power_plants,
                                                             losses,
                                                             populated_areas,
                                                             num_populated_areas,
                                                             num_power_plants)

    if num_not_enough_energy > 0:
        if price < most_expensive_plant:
            price = most_expensive_plant
        price *= (num_not_enough_energy + 1)

    if print_to_console:
        print "Chromo:", proposed_distribution
        print "Num over capacity: ", num_over_capacity, \
            " Num grid violations", num_errors_for_grid_violation, \
            "Num areas not enough power:", num_not_enough_energy, \
            " Calculated price: ", price

    return price


def create_eval_function(power_plants, losses, populated_areas, print_to_console=False):
    def eval_in(chromosome):
        return eval_function(chromosome, power_plants, losses, populated_areas, print_to_console)

    return eval_in


def execute_example(test_example, ga_properties):
    if not isinstance(test_example, TestExample):
        raise ValueError("Only instances of TestExample are accepted for the first argument")
    if not isinstance(ga_properties, GAProperties):
        raise ValueError("Only instances of GAProperties are accepted for the second argument")

    num_populated_areas = test_example.get_num_cities()
    num_power_plants = test_example.get_num_power_plants()
    reqs_pop = test_example.get_power_requirements()
    populated_areas = []
    for i in xrange(num_populated_areas):
        populated_areas.append(PopulatedArea(reqs_pop[i]))

    power_plants = []
    for plant in xrange(num_power_plants):
        power_plants.append(PowerPlant(test_example.get_max_production_capacity()[plant],
                                       test_example.get_price_at_max_capacity()[plant]))

    losses = test_example.get_loss_matrix()
    eval_function_generated = create_eval_function(power_plants, losses, populated_areas)
    genome = ProposedDistributionGenomeV2(losses)
    genome.evaluator.set(eval_function_generated)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(ga_properties.generations)
    ga.setPopulationSize(ga_properties.pop_size)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(ga_properties.cross_rate)
    ga.setMutationRate(ga_properties.mut_rate)
    ga.setElitism(True)
    ga.setElitismReplacement(ga_properties.elit_replacement)
    ga.evolve(freq_stats=5000)
    print "--------------"
    print ga.bestIndividual().proposed_distribution
    print eval_function(ga.bestIndividual(), power_plants, losses, populated_areas, print_to_console=True)


if __name__ == '__main__':
    test_examples = {#"1a": TestExample1a(),
                    # "1b": TestExample1b(),
                    #  "1c": TestExample1c(),
                    #  "2a": TestExample2a(),
                    #  "2b": TestExample2b(),
                    #  "2c": TestExample2c()
                    "3a": TestExample3a() }

    properties = GAProperties(generations=15000, pop_size=1000, cross_rate=0.5, mut_rate=0.35, elit_replacement=5)
    for example_name in test_examples.keys():
        print "-------------"
        print example_name
        execute_example(test_examples[example_name], properties)
        print "-------------"
