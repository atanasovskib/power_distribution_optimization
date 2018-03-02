from test_examples.TestExample import TestExample


class TestExample2a(TestExample):
    def __init__(self):
        TestExample.__init__(self)
        self.required_power = [150, 200]
        self.max_proiz = [250, 200]
        self.max_cena = [120, 50]
        self.zaguba = [[10, 10], [10, 10]]

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
