import unittest
from pladmed.models.connection import Connection

class ConnectionTest(unittest.TestCase):
    def setUp(self):
        self.conn = Connection(
            conn="Socket"
        )

    def test_connection_includes_alive_state(self):
        self.assertEqual(True, self.conn.alive)

    def test_connection_disconnect(self):
        self.conn.disconnect()

        self.assertEqual(False, self.conn.alive)
