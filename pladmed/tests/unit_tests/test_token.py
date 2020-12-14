import unittest
from pladmed.models.token import Token

class TokenTest(unittest.TestCase):
    def setUp(self):
        self.token = Token(secret_key="secret_key")

    def test_token_has_secret_key(self):
        self.assertEqual(self.token.secret_key, "secret_key")
