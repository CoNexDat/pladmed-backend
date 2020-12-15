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

    def test_receives_traceroute(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        self.client.post('/traceroute', json=dict(
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

    def test_receives_ping(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        self.client.post('/ping', json=dict(
            operation="ping",
            probes=["identifier"],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"]
            }
        ))

        received = probe.get_received()

        self.assertEqual(received[0]["name"], "ping")
        self.assertEqual(received[0]["args"][0]["params"]["ips"][0], "192.168.0.0")

    def test_receives_dns(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        self.client.post('/dns', json=dict(
            operation="dns",
            probes=["identifier"],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"]
            }
        ))

        received = probe.get_received()

        self.assertEqual(received[0]["name"], "dns")
        self.assertEqual(received[0]["args"][0]["params"]["ips"][0], "192.168.0.0")

    def test_register_probe_correctly(self):
        res = self.client.post('/probes')

        self.assertEqual(res.status_code, 201)
