import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class CreditsTest(BaseTest):
    def test_give_credits_requires_superuser(self):
        self.access_token = self.register_user()

        res = self.client.post('/credits',
            json=dict(
                id="some_id",
                credits=10
            ),
            headers={'access_token': self.access_token}
        )

        self.assertEqual(res.status_code, 401)
