import jwt

class Token:
    def __init__(self, secret_key):
        self.secret_key = secret_key
