import jwt

class Token:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_token(self, identity):
        token = jwt.encode(identity, self.secret_key, algorithm='HS256').decode('utf-8')
        return token
    
    def identity(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except:
            return None
