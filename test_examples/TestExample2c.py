from test_examples.TestExample import TestExample


class TestExample2c(TestExample):
    def __init__(self):
        TestExample.__init__(self)
        self.required_power = [100, 100, 100, 100, 100, 100, 100]
        self.max_production_capacity = [300, 150, 300, 150]
        self.price_at_max_capacity = [100, 80, 60, 40]
        self.loss_matrix = [[0, 10, 10, 10],
                            [10, 0, 10, 10],
                            [10, 10, 0, 10],
                            [10, 10, 10, 0],
                            [0, 0, 5, 5],
                            [5, 5, 0, 0],
                            [10, 10, 10, 10]]

    def get_power_requirements(self):
        return self.required_power

    def get_max_production_capacity(self):
        return self.max_production_capacity

    def get_price_at_max_capacity(self):
        return self.price_at_max_capacity

    def get_loss_matrix(self):
        return self.loss_matrix

    def get_num_power_plants(self):
        return len(self.price_at_max_capacity)

    def get_num_cities(self):
        return len(self.required_power)
