import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class UserTest(BaseTest):
    def register_user(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        res = self.client.post('/login', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        self.token = json.loads(res.data)["access_token"]

    def test_get_user_data(self):
        self.register_user()

        res = self.client.get(
            '/users/me', 
            headers={'access_token': self.token}
        )

        self.assertEqual(res.status_code, 200)

    def test_get_user_data_fails_no_token(self):
        self.register_user()

        res = self.client.get(
            '/users/me'
        )

        self.assertEqual(res.status_code, 403)

    def test_get_user_data_fails_invalid_token(self):
        self.register_user()

        res = self.client.get(
            '/users/me',
            headers={'access_token': "invalid_token"}
        )

        self.assertEqual(res.status_code, 403)
