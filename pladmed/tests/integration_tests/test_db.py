import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
from pladmed.models.user import User
from passlib.hash import pbkdf2_sha256 as secure_password
import json

class DatabaseTest(BaseTest):
    def test_creates_users(self):
        user = self.app.db.users.create_user("juan@gmail.com", "123")

        self.assertEqual(user.email, "juan@gmail.com")

    def test_gets_no_user_if_not_created(self):
        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertEqual(user, None)

    def test_find_users(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertEqual(user.email, "juan@gmail.com")        

    def test_reset_db(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        self.app.db.reset_db()

        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertEqual(user, None)

    def test_password_is_secure(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertNotEqual(user.password, "123")
        self.assertEqual(secure_password.verify("123", user.password), True)
