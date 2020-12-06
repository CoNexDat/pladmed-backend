import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class AuthenticationTest(BaseTest):
    def test_register_user(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        self.assertEqual(res.status_code, 201)

    def test_register_user_doesnt_return_password(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        data = json.loads(res.data)

        self.assertEqual(data["email"], "agustin@gmail.com")
        self.assertEqual("password" in data, False)
        
    def test_unique_users(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        self.assertEqual(res.status_code, 404)
