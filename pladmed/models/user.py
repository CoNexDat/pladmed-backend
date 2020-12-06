class User:
    def __init__(self, _id, email, password):
        self._id = _id
        self.email = email
        self.password = password

    def public_data(self):
        data = self.__dict__
        del data["password"]

        return data
