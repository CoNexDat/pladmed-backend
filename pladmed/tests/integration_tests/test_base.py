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

    def register_user(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        res = self.client.post('/login', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        return json.loads(res.data)["access_token"]    

    def register_probe(self, token):
        res = self.client.post(
            '/probes',
            headers={'access_token': token}
        )

        data = json.loads(res.data)

        return data["token"]
