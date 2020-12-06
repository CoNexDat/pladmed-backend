from passlib.hash import pbkdf2_sha256 as secure_password

class User:
    def __init__(self, params):
        # TODO Validate params

        for param in params:
            setattr(self, param, params[param])

        if "raw_password" in params:
            self.password = secure_password.hash(self.raw_password)
            del self.raw_password

    def verify_password(self, password):
        return secure_password.verify(password, self.password)

    def public_data(self):
        data = self.__dict__
        del data["password"]

        return data
