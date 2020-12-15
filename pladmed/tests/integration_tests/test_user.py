import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class UserTest(BaseTest):
    def test_get_user_data(self):
        access_token = self.register_user()

        res = self.client.get(
            '/users/me', 
            headers={'access_token': access_token}
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
            headers={
                'access_token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXIifQ.Q-JpIizU5ITl167RI6oN7R8kvCWrfGasBxARnIyJQv1"
            }
        )

        self.assertEqual(res.status_code, 403)

    def test_get_user_data_returns_user_data(self):
        access_token = self.register_user()

        res = self.client.get(
            '/users/me', 
            headers={'access_token': access_token}
        )

        data = json.loads(res.data)

        expected_data = (
            "_id",
            "email"
        )
        
        self.assertEqual(len(expected_data - data.keys()), 0)