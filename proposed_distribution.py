class ProposedDistribution:
    def __init__(self, distribution):
        if type(distribution) is not list:
            raise ValueError("distribution should be a matrix of integers")

        if len(distribution) <= 0:
            raise ValueError("there should be at least one row in the matrix")

        expected_length = distribution[0]
        if expected_length <= 0:
            raise ValueError("there should be at least one column in each row")

        any_item_is_not_list = any([type(x) is not list for x in distribution])
        if any_item_is_not_list:
            raise ValueError("distribution is not a matrix of integers")

        for row in distribution:
            if len(row) != expected_length:
                raise ValueError("all rows must have the same number of columns")

            for item in row:
                if type(item) is not int or item <= 0 or item >= 100:
                    raise ValueError("each item in the distribution matrix must be an integer > 0 and < 100")

        self.distribution = distribution

    def clone(self):
        new_distribution = [row[:] for row in self.distribution]

        return ProposedDistribution(new_distribution)
