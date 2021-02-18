class Operation:
    def __init__(self, _id, operation, params, probes):
        self._id = _id
        self.operation = operation
        self.probes = probes
        self.params = params
        self.results = []

    def public_data(self):
        data = self.__dict__

        del data["operation"]

        return data
