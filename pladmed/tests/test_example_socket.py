import unittest
from pladmed.tests.test_base import BaseTest
import json
from pladmed import socketio

class ExampleTest(BaseTest):
    def test_socket(self):
        #Start connection
        client_socket = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        #Ensure connection is up
        #assert client_socket.is_connected()

        r = client_socket.get_received()

        self.assertEqual(r[0]['name'], 'connected')
