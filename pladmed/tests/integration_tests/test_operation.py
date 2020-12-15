import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json

class OperationTest(BaseTest):
    def test_creates_traceroute(self):
        res = self.client.post('/traceroute', json=dict(
            operation="traceroute",
            probes=["test_probe", "another_test_probe"],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ))

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

    def test_creates_ping(self):
        res = self.client.post('/ping', json=dict(
            operation="ping",
            probes=["test_probe", "another_test_probe"],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ))

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

    def test_creates_dns(self):
        res = self.client.post('/dns', json=dict(
            operation="dns",
            probes=["test_probe", "another_test_probe"],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"]
            }
        ))

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

