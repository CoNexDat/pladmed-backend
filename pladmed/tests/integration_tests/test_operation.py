import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json


class OperationTest(BaseTest):
    def setUp(self):
        super().setUp()

        self.access_token = self.register_user()
        self.probe_conn = self.start_connection(self.access_token)

    def tearDown(self):
        try:
            self.probe_conn.disconnect()
        except:
            pass

        super().tearDown()

    def test_creates_traceroute(self):
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
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertEqual(data["params"]["confidence"], 0.95)

    def test_creates_ping(self):
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
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

    def test_creates_dns(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=[probes[0]["identifier"]],
                params={
                    "domains": ["www.google.com", "www.facebook.com"]
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)

    def test_creates_traceroute_requires_login(self):
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

        self.assertEqual(401, res.status_code)

    def test_creates_ping_requires_login(self):
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

        self.assertEqual(401, res.status_code)

    def test_creates_dns_requires_login(self):
        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=["test_probe", "another_test_probe"],
                params={
                    "dns": ["www.google.com", "www.facebook.com"]
                }
            )
        )

        data = json.loads(res.data)

        self.assertEqual(401, res.status_code)

    def test_creates_traceroute_returns_404_invalid_probes(self):
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
            headers={'access_token': self.access_token}
        )

        self.assertEqual(404, res.status_code)

    def test_create_traceroute_fails_without_ips_or_dns(self):
        self.create_operation_fails_without_ips_or_dns("traceroute")

    def test_create_ping_fails_without_ips_or_dns(self):
        self.create_operation_fails_without_ips_or_dns("ping")

    def test_create_dns_fails_without_ips_or_dns(self):
        self.create_operation_fails_without_ips_or_dns("dns")

    def create_operation_fails_without_ips_or_dns(self, operation):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            f'/{operation}',
            json=dict(
                operation=operation,
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "domains": []
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_creates_traceroute_saves_operation_in_db(self):
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
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        operation = self.app.db.operations.find_operation(data["_id"])

        self.assertEqual(operation.operation, "traceroute")

    def test_creates_ping_saves_operation_in_db(self):
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
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        operation = self.app.db.operations.find_operation(data["_id"])

        self.assertEqual(operation.operation, "ping")

    def test_creates_ping_returns_404_invalid_probes(self):
        res = self.client.post(
            '/ping',
            json=dict(
                probes=["test_probe", "another_test_probe"],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': self.access_token}
        )

        self.assertEqual(404, res.status_code)

    def test_creates_dns_saves_operation_in_db(self):
        probes = self.app.db.probes.find_all_probes()

        res = self.client.post(
            '/dns',
            json=dict(
                probes=[probes[0].identifier],
                params={
                    "domains": ["www.google.com", "www.facebook.com"]
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        operation = self.app.db.operations.find_operation(data["_id"])

        self.assertEqual(operation.operation, "dns")

    def test_creates_dns_returns_404_invalid_probes(self):
        res = self.client.post(
            '/dns',
            json=dict(
                probes=["test_probe", "another_test_probe"],
                params={
                    "domains": ["www.google.com", "www.facebook.com"]
                }
            ),
            headers={'access_token': self.access_token}
        )

        self.assertEqual(404, res.status_code)

    def test_creates_traceroute_returns_error_if_no_avail_probe(self):
        self.probe_conn.disconnect()

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
            headers={'access_token': self.access_token}
        )

        self.assertEqual(404, res.status_code)

    def test_creates_traceroute_returns_only_avail_probes(self):
        self.register_probe(self.access_token)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"], probes[1]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(1, len(data["probes"]))

    def test_get_operation(self):
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
            headers={'access_token': self.access_token}
        )

        data_op = json.loads(res.data)

        params = {
            'id': data_op["_id"]
        }

        res = self.client.get(
            '/operation',
            query_string=params
        )

        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(data["_id"], data_op["_id"])

    def test_get_operation_fails_with_bad_id(self):
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
            headers={'access_token': self.access_token}
        )

        data_op = json.loads(res.data)

        params = {
            'id': "a fake id"
        }

        res = self.client.get(
            '/operation',
            query_string=params
        )

        self.assertEqual(404, res.status_code)

    def test_get_operation_fails_with_no_id(self):
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
            headers={'access_token': self.access_token}
        )

        data_op = json.loads(res.data)

        res = self.client.get(
            '/operation'
        )

        self.assertEqual(404, res.status_code)

    def test_creates_traceroute_includes_credits_per_operation(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/traceroute',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(data["credits"], 30)

    def test_creates_ping_includes_credits_per_operation(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/ping',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"]
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(data["credits"], 2)

    def test_creates_dns_includes_credits_per_operation(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/dns',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "domains": ["www.google.com", "www.facebook.com"]
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(data["credits"], 2)

    def test_creates_operation_includes_credits_per_probe(self):
        probe_conn = self.start_connection(self.access_token)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/dns',
            json=dict(
                probes=[probes[0]["identifier"], probes[1]["identifier"]],
                params={
                    "domains": ["www.google.com", "www.facebook.com"]
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(data["credits"], 4)

        probe_conn.disconnect()

    def test_creates_operation_includes_credits_per_probe_available(self):
        self.register_probe(self.access_token)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/dns',
            json=dict(
                probes=[probes[0]["identifier"], probes[1]["identifier"]],
                params={
                    "domains": ["www.google.com", "www.facebook.com"]
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(data["credits"], 2)

    def test_creates_operation_removes_probe_not_enough_credits(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/traceroute',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [
                        "192.168.1.0", "192.168.1.0",
                        "192.168.1.0", "192.168.1.0"
                    ]
                }
            ),
            headers={'access_token': self.access_token}
        )

        self.assertEqual(res.status_code, 404)

    def test_creates_traceroute_fails_without_enough_credits(self):
        user = self.app.db.users.find_user("agustin@gmail.com")
        self.app.db.users.change_credits(user, 5)

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
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(400, res.status_code)

    def test_creates_operation_changes_credits_for_user(self):
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
            headers={'access_token': self.access_token}
        )

        user = self.app.db.users.find_user("agustin@gmail.com")

        self.assertEqual(user.credits, 370)
