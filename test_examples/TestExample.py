from abc import abstractmethod


class TestExample:

    def __init__(self):
        pass

    @abstractmethod
    def get_power_requirements(self):
        pass

    @abstractmethod
    def get_max_production_capacity(self):
        pass

    @abstractmethod
    def get_price_at_max_capacity(self):
        pass

    @abstractmethod
    def get_loss_matrix(self):
        pass

    @abstractmethod
    def get_num_power_plants(self):
        pass

    @abstractmethod
    def get_num_cities(self):
        pass
