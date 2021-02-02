import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json
from pladmed import socketio

class ProbeTest(BaseTest):
    def start_connection(self, access_token):
        token = self.register_probe(access_token)

        query = "token=" + token

        return socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string=query
        )

    def test_connection_up(self):
        access_token = self.register_user()
        probe = self.start_connection(access_token)

        self.assertEqual(len(self.app.probes), 1)

    def test_disconnect(self):
        access_token = self.register_user()
        probe = self.start_connection(access_token)

        probe.disconnect()

        self.assertEqual(len(self.app.probes), 0)

    def test_receives_traceroute(self):
        access_token = self.register_user()
        probe = self.start_connection(access_token)

        res = self.client.get('/probes')

        probes = json.loads(res.data)

        self.client.post('/traceroute', json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': access_token}
        )

        received = probe.get_received()

        self.assertEqual(received[0]["name"], "traceroute")
        self.assertEqual(received[0]["args"][0]["params"]["ips"][0], "192.168.0.0")

    def test_receives_ping(self):
        access_token = self.register_user()
        probe = self.start_connection(access_token)

        res = self.client.get('/probes')

        probes = json.loads(res.data)

        self.client.post('/ping', json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"]
                }
            ),
            headers={'access_token': access_token}
        )

        received = probe.get_received()

        self.assertEqual(received[0]["name"], "ping")
        self.assertEqual(received[0]["args"][0]["params"]["ips"][0], "192.168.0.0")

    def test_receives_dns(self):
        access_token = self.register_user()
        probe = self.start_connection(access_token)
        
        res = self.client.get('/probes')

        probes = json.loads(res.data)

        self.client.post('/dns', json=dict(
            operation="dns",
            probes=[probes[0]["identifier"]],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"]
            }
        ))

        received = probe.get_received()

        self.assertEqual(received[0]["name"], "dns")
        self.assertEqual(received[0]["args"][0]["params"]["ips"][0], "192.168.0.0")

    def test_connection_refuse_no_token(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client
        )

        self.assertEqual(len(self.app.probes), 0)

    def test_connection_refuse_invalid_token(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string="token=fake_token"
        )

        self.assertEqual(len(self.app.probes), 0)

    def test_connection_refuse_fake_token(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string="token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiNWZkODkwZWIxOTIxMGUxODg0ZWU5NDRmIn0.lcyp89G7GobSTe8qQnCNmDKNFFl1jRtyAWymlWJWpa4"
        )

        self.assertEqual(len(self.app.probes), 0)

    # ---------------------------------------------
    # API Rest test
    # ---------------------------------------------

    def test_register_probe_correctly(self):
        access_token = self.register_user()

        res = self.client.post(
            '/probes',
            headers={'access_token': access_token}
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
        access_token = self.register_user()
        token = self.register_probe(access_token)

        self.assertEqual(len(token) > 0, True)

    def test_get_all_probes(self):
        access_token = self.register_user()
        self.register_probe(access_token)

        res = self.client.get(
            '/probes'
        )

        data = json.loads(res.data)

        self.assertEqual(len(data), 1)

    def test_get_all_probes_zero_if_not_created(self):
        res = self.client.get(
            '/probes'
        )

        data = json.loads(res.data)

        self.assertEqual(len(data), 0)
