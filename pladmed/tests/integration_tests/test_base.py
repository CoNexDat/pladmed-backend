import unittest
from pladmed import create_app
from pladmed import socketio
import json


class BaseTest(unittest.TestCase):
    def setUp(self):
        # It would be better to use setUpClass
        self.app = create_app({"TESTING": True, "MONGO_DB": "testing_db"})
        self.client = self.app.test_client()

    def tearDown(self):
        self.app.db.reset_db()

    def register_superuser(self):
        user = self.app.db.users.create_user(
            email="diego.lopez@gmail.com",
            password="seCure123!",
            is_superuser=True,
            credits_=400
        )

        res = self.client.post('/login', json=dict(
            email="diego.lopez@gmail.com",
            password="seCure123!"
        ))

        return json.loads(res.data)["access_token"]

    def register_predefined_user(self):
        return self.register_user("agustin@gmail.com", "secure_Password1")

    def register_user(self, email, password):
        self.client.post('/register', json=dict(
            email=email,
            password=password
        ))

        res = self.client.post('/login', json=dict(
            email=email,
            password=password
        ))

        user = self.app.db.users.find_user(email)
        self.app.db.users.change_credits(user, 400)

        return json.loads(res.data)["access_token"]

    def register_probe(self, token, location):
        res = self.client.post(
            '/probes',
            headers={'access_token': token},
            json=dict(location=location)
        )

        data = json.loads(res.data)
        return data["token"]

    def start_connection(self, access_token, location):
        token = self.register_probe(access_token, location)

        query = "token=" + token

        return socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string=query,
            headers={"total_credits": 40, "in_use_credits": 0}
        )
