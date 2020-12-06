import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class UserTest(BaseTest):
    def test_create_user(self):
        res = self.client.post('/users', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        self.assertEqual(res.status_code, 201)

    def test_create_user_doesnt_return_password(self):
        res = self.client.post('/users', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        data = json.loads(res.data)

        self.assertEqual(data["email"], "agustin@gmail.com")
        self.assertEqual("password" in data, False)
