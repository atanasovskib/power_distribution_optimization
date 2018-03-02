class PowerPlant:
    def __init__(self, production_at_max_capacity, price_at_max_capacity):
        if type(production_at_max_capacity) is not int:
            raise ValueError("production_at_max_capacity must be an integer")

        if production_at_max_capacity < 0:
            raise ValueError("production_at_max_capacity can not be negative")

        if price_at_max_capacity < 0:
            raise ValueError("price at max capacity can not be negative")
        self.production_at_max_capacity = production_at_max_capacity
        self.price_at_max_capacity = float(price_at_max_capacity)

    def price_at_capacity(self, capacity):
        if type(capacity) is not int:
            raise ValueError("capacity must be an integer")

        if capacity < 0 or capacity > 100 or capacity % 10 != 0:
            raise ValueError("capacity must be >=0, <=100 and divisible by 10")

        return self.price_at_max_capacity * capacity / 100.0


class AvailablePowerPlants:
    def __init__(self, plants):
        if type(plants) is not list:
            raise ValueError("plants are supposed to be a list")

        any_item_is_not_a_plant = any([not isinstance(x, PowerPlant) for x in plants])
        if any_item_is_not_a_plant:
            raise ValueError("some of the objects in the plants list are not PowerPlants")

        self.plants = plants

    def __getitem__(self, item):
        return self.plants[item]
