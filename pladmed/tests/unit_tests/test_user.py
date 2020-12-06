import unittest
from pladmed.models.user import User
from passlib.hash import pbkdf2_sha256 as secure_password

class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = User(
            _id="482932jik",
            email="agustin@gmail.com",
            password=secure_password.hash("simple_password")
        )

    def test_user_has_id(self):
        self.assertEqual(self.user._id, "482932jik")

    def test_user_has_email(self):
        self.assertEqual(self.user.email, "agustin@gmail.com")

    def test_user_has_password(self):
        self.assertEqual(
            secure_password.verify(
                "simple_password",
                self.user.password
            ),
            True
        )
    
