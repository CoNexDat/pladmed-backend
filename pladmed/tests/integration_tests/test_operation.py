import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class OperationTest(BaseTest):
    def test_creates_traceroute(self):
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

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

    def test_creates_ping(self):
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
