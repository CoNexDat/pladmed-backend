import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json
from pladmed import socketio

class ProbeTest(BaseTest):
    def start_connection(self):
        return socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string="token=single_token"
        )

    def test_connection_up(self):
        probe = self.start_connection()

        self.assertEqual(len(self.app.probes), 1)

    def test_disconnect(self):
        probe = self.start_connection()

        probe.disconnect()

        self.assertEqual(len(self.app.probes), 0)

    def test_receives_traceroute(self):
        probe = self.start_connection()

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
        probe = self.start_connection()

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
        probe = self.start_connection()

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
        self.register_user()

        res = self.client.post(
            '/probes',
            headers={'access_token': self.token}
        )

        self.assertEqual(res.status_code, 201)

    def test_register_probe_doesnt_work_without_token(self):
        res = self.client.post('/probes')

        self.assertEqual(res.status_code, 403)

    def test_register_probe_doesnt_work_without_invalid_token(self):
        res = self.client.post(
            '/probes',
            headers={'access_token': "fake_token"}
        )

        self.assertEqual(res.status_code, 403)

    def test_register_probe_correctly_gets_token(self):
        self.register_user()

        res = self.client.post(
            '/probes',
            headers={'access_token': self.token}
        )

        data = json.loads(res.data)

        self.assertEqual("token" in data, True)
