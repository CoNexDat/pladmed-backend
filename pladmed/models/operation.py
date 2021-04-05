class Operation:
    def __init__(self, _id, operation, params, probes, credits_, result_format):
        self._id = _id
        self.operation = operation
        self.probes = probes
        self.params = params
        self.results = []
        self.credits = credits_
        self.result_format = result_format

    def public_data(self):
        data = self.__dict__.copy()

        del data["operation"]

        for result in data["results"]:
            del result["unique_code"]

        return data

    def add_results(self, probe, results, unique_code):
        new_results = {
            "probe": probe,
            "results": results,
            "unique_code": unique_code
        }

        self.results.append(new_results)

    def code_exists(self, code):
        for result in self.results:
            if code == result["unique_code"]:
                return True

        return False
