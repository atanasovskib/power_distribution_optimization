class PopulatedArea:
    def __init__(self, consumed_electricity):
        if type(consumed_electricity) is not int:
            raise ValueError("consumed_electricity must be an integer")

        if consumed_electricity < 0:
            raise ValueError("production_at_max_capacity can not be negative")

        self.consumed_electricity = consumed_electricity


class Area:
    def __init__(self, populated_areas):
        if type(populated_areas) is not list:
            raise ValueError("populated_areas is supposed to be a list")

        any_item_is_not_a_pop_area = any([not isinstance(x, PopulatedArea) for x in populated_areas])
        if any_item_is_not_a_pop_area:
            raise ValueError("some of the objects in the plants list are not PowerPlants")

        self.populated_areas = populated_areas

    def __getitem__(self, item):
        return self.populated_areas[item]
