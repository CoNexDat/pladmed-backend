import unittest
from pladmed.models.user import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = User(
            email="agustin@gmail.com",
            password="simple_password"
        )

    def test_user_has_email(self):
        self.assertEqual(self.user.email, "agustin@gmail.com")

    def test_user_has_password(self):
        self.assertEqual(self.user.password, "simple_password")
