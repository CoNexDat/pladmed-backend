import unittest
from pladmed import create_app
from pladmed import socketio

class BaseTest(unittest.TestCase):
    def setUp(self):
        # It would be better to use setUpClass
        self.app = create_app({"TESTING": True, "MONGO_DB": "testing_db"})
        self.client = self.app.test_client()

    def tearDown(self):
        self.app.db.reset_db()
