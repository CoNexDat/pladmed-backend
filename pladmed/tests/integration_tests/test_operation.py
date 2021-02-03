import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class OperationTest(BaseTest):
    def test_creates_traceroute(self):
        access_token = self.register_user()
        self.register_probe(access_token)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/traceroute', 
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertEqual(data["params"]["confidence"], 0.95)
        self.assertEqual(data["probes"][0]["identifier"], probes[0]["identifier"])

    def test_creates_ping(self):
        access_token = self.register_user()
        self.register_probe(access_token)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/ping', 
            json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

    def test_creates_dns(self):
        access_token = self.register_user()

        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=["test_probe", "another_test_probe"],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"]
                }
            ),
            headers={'access_token': access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

    def test_creates_traceroute_requires_login(self):
        access_token = self.register_user()

        res = self.client.post(
            '/traceroute', 
            json=dict(
                operation="traceroute",
                probes=["test_probe", "another_test_probe"],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            )
        )

        data = json.loads(res.data)

        self.assertEqual(403, res.status_code)

    def test_creates_ping_requires_login(self):
        access_token = self.register_user()

        res = self.client.post(
            '/ping', 
            json=dict(
                operation="ping",
                probes=["test_probe", "another_test_probe"],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            )
        )

        data = json.loads(res.data)

        self.assertEqual(403, res.status_code)

    def test_creates_dns_requires_login(self):
        access_token = self.register_user()

        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=["test_probe", "another_test_probe"],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"]
                }
            )
        )

        data = json.loads(res.data)

        self.assertEqual(403, res.status_code)

    def test_creates_traceroute_returns_404_invalid_probes(self):
        access_token = self.register_user()

        res = self.client.post(
            '/traceroute', 
            json=dict(
                operation="traceroute",
                probes=["test_probe", "another_test_probe"],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': access_token}
        )

        self.assertEqual(404, res.status_code)

    def test_creates_traceroute_saves_operation_in_db(self):
        access_token = self.register_user()
        self.register_probe(access_token)

        probes = self.app.db.probes.find_all_probes()

        res = self.client.post(
            '/traceroute', 
            json=dict(
                operation="traceroute",
                probes=[probes[0].identifier],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': access_token}
        )

        data = json.loads(res.data)

        operation = self.app.db.operations.find_operation(data["_id"])

        self.assertEqual(operation.operation, "traceroute")

    def test_creates_ping_saves_operation_in_db(self):
        access_token = self.register_user()
        self.register_probe(access_token)

        probes = self.app.db.probes.find_all_probes()

        res = self.client.post(
            '/ping', 
            json=dict(
                probes=[probes[0].identifier],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': access_token}
        )

        data = json.loads(res.data)

        operation = self.app.db.operations.find_operation(data["_id"])

        self.assertEqual(operation.operation, "ping")
