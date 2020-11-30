import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json
from pladmed import socketio

class ProbeTest(BaseTest):
    def test_connection_up(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        self.assertEqual(len(self.app.probes), 1)

        probe.disconnect()

    def test_disconnect(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        probe.disconnect()

        self.assertEqual(len(self.app.probes), 0)
