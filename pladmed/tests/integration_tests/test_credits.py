import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json


class CreditsTest(BaseTest):
    def test_give_credits_requires_superuser(self):
        access_token = self.register_predefined_user()

        res = self.client.post('/credits',
                               json=dict(
                                   id="some_id",
                                   credits=10
                               ),
                               headers={'access_token': access_token}
                               )

        self.assertEqual(res.status_code, 401)

    def test_give_credits_to_user(self):
        access_token = self.register_superuser()

        user = self.app.db.users.find_user("diego.lopez@gmail.com")

        res = self.client.post('/credits',
                               json=dict(
                                   id=user._id,
                                   credits=10
                               ),
                               headers={'access_token': access_token}
                               )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["credits"], 410)

    def test_give_credits_to_fake_user_returns_error(self):
        access_token = self.register_superuser()

        user = self.app.db.users.find_user("diego@gmail.com")

        res = self.client.post('/credits',
                               json=dict(
                                   id="nice fake user",
                                   credits=10
                               ),
                               headers={'access_token': access_token}
                               )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_give_credits_should_have_userId(self):
        access_token = self.register_superuser()

        user = self.app.db.users.find_user("diego@gmail.com")

        res = self.client.post('/credits',
                               json=dict(
                                   credits=10
                               ),
                               headers={'access_token': access_token}
                               )

        self.assertEqual(res.status_code, 400)

    def test_give_credits_should_have_credits_amount(self):
        access_token = self.register_superuser()

        user = self.app.db.users.find_user("diego@gmail.com")

        res = self.client.post('/credits',
                               json=dict(
                                   id="nice fake user"
                               ),
                               headers={'access_token': access_token}
                               )

        self.assertEqual(res.status_code, 400)
