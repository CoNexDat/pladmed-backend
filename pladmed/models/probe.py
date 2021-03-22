class Probe:
    def __init__(self, identifier, owner_id=None, location=None):
        self.identifier = identifier
        self.owner_id = owner_id
        self.location = location

    def public_data(self):
        data = self.__dict__.copy()

        return data

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier
