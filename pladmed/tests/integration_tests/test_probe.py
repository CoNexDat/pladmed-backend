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

    def test_disconnect(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        probe.disconnect()

        self.assertEqual(len(self.app.probes), 0)

    def test_receives_operation(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        self.client.post('/operation', json=dict(
            operation="traceroute",
            probes=["identifier"],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ))

        received = probe.get_received()

        self.assertEqual(received[0]["name"], "traceroute")
        self.assertEqual(received[0]["args"][0]["params"]["ips"][0], "192.168.0.0")
