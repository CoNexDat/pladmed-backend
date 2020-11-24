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

        client_socket.emit('test_event', {"data": "something"})

        r = client_socket.get_received()

        self.assertEqual(r[0]['name'], 'connected')
        self.assertEqual(r[1]['name'], 'response')
        self.assertEqual(r[1]['args'][0]["data"], 'something')