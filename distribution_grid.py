class DistributionGrid:
    def __init__(self, losses):
        if type(losses) is not list:
            raise ValueError("losses is not a matrix of integers")

        any_item_is_not_list = any([type(x) is not list for x in losses])
        if any_item_is_not_list:
            raise ValueError("losses is not a matrix of integers")

        for row in losses:
            for item in row:
                if type(item) is not int or item < 0 or item >= 100:
                    raise ValueError("each item in the losses matrix must be an integer > 0 and < 100")

        self.losses = losses
