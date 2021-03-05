class Probe:
    def __init__(self, identifier, total_credits):
        self.identifier = identifier
        self.total_credits = total_credits

    def public_data(self):
        data = self.__dict__.copy()

        return data

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier
