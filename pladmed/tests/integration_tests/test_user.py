import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class UserTest(BaseTest):
    def register_user(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        self.token = self.client.post('/login', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

    def test_get_user_data(self):
        self.register_user()

        res = self.client.get(
            '/users/me', 
            headers={'access_token': self.token}
        )

        self.assertEqual(res.status_code, 200)
