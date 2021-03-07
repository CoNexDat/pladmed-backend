class Probe:
    def __init__(self, identifier):
        self.identifier = identifier
        self.total_credits = None
        self.in_use_credits = 0

    def public_data(self):
        data = self.__dict__.copy()

        del data["total_credits"]
        del data["in_use_credits"]

        return data

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier
