from test_examples.TestExample import TestExample


class TestExample1a(TestExample):
    def __init__(self):
        TestExample.__init__(self)
        self.required_power = [10, 20, 50, 100, 30, 40, 100, 5, 10, 20]
        self.max_proiz = [500]
        self.max_cena = [1000]
        self.zaguba = [[10], [10], [10], [10], [10], [10], [10], [10], [10], [10]]

    def get_power_requirements(self):
        return self.required_power

    def get_max_production_capacity(self):
        return self.max_proiz

    def get_price_at_max_capacity(self):
        return self.max_cena

    def get_loss_matrix(self):
        return self.zaguba

    def get_num_power_plants(self):
        return len(self.max_cena)

    def get_num_cities(self):
        return len(self.required_power)
