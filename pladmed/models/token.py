import jwt

class Token:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_token(self, identity):
        return jwt.encode(identity, self.secret_key, algorithm='HS256')
    
    def identity(self, token):
        return jwt.decode(token, self.secret_key, algorithms=['HS256'])
