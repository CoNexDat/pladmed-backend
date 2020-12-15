import unittest
from pladmed.models.token import Token

class TokenTest(unittest.TestCase):
    def setUp(self):
        self.token = Token(secret_key="secret_key")

    def test_token_has_secret_key(self):
        self.assertEqual(self.token.secret_key, "secret_key")

    def test_token_encodes_identity(self):
        identity = {
            "email": "agustin@gmail.com"
        }
        
        token = self.token.create_token(identity)

        ret_identity = self.token.identity(token)

        self.assertEqual(identity["email"], ret_identity["email"])
