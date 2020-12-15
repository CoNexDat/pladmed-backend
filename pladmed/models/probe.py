class Probe:
    def __init__(self, identifier):
        self.identifier = identifier

    def public_data(self):
        data = self.__dict__

        return data
