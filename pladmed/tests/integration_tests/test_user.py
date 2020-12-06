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
