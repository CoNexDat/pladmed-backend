import unittest
from pladmed.models.user import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = User({
            "_id": "482932jik",
            "email": "agustin@gmail.com"
        })

        self.user.set_password("simple_password")

    def test_user_has_id(self):
        self.assertEqual(self.user._id, "482932jik")

    def test_user_has_email(self):
        self.assertEqual(self.user.email, "agustin@gmail.com")

    def test_user_has_password(self):
        self.assertEqual(
            self.user.verify_password("simple_password"),
            True
        )
    
