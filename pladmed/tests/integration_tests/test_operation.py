from os import truncate
import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json
from datetime import datetime, time, timedelta

# TODO Reduce code duplication


class OperationTest(BaseTest):
    LOCATION = {"longitude": 58.411217, "latitude": 40.181038}

    def setUp(self):
        super().setUp()

        self.access_token = self.register_predefined_user()
        self.probe_conn = self.start_connection(
            self.access_token, self.LOCATION)

    def tearDown(self):
        try:
            self.probe_conn.disconnect()
        except:
            pass

        super().tearDown()

    def test_creates_traceroute(self):
        self.create_operation("traceroute", {
            "ips": ["192.168.0.0", "192.162.1.1"],
            "confidence": 0.95,
            "cron": "* * * * *",
            "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "times_per_minute": 1
        })

    def test_creates_ping(self):
        self.create_operation("ping", {
            "ips": ["192.168.0.0", "192.162.1.1"],
            "cron": "* * * * *",
            "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "times_per_minute": 1
        })

    def test_creates_dns(self):
        self.create_operation("dns", {
            "fqdns": ["www.google.com", "www.facebook.com"],
            "cron": "* * * * *",
            "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "times_per_minute": 1
        })

    def create_operation(self, operation, params):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            f"/{operation}",
            json=dict(
                operation=f"{operation}",
                probes=[probes[0]["identifier"]],
                params=params,
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)
        self.assertEqual(201, res.status_code)

    def test_creates_traceroute_requires_login(self):
        self.create_operation_requires_login("traceroute")

    def test_creates_ping_requires_login(self):
        self.create_operation_requires_login("ping")

    def test_creates_dns_requires_login(self):
        self.create_operation_requires_login("dns")

    def create_operation_requires_login(self, operation):
        res = self.client.post(
            f"/{operation}",
            json=dict(
                operation=f"{operation}",
                probes=["test_probe", "another_test_probe"]
            )
        )
        json.loads(res.data)
        self.assertEqual(401, res.status_code)

    def test_creates_traceroute_returns_404_invalid_probes(self):
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=["test_probe", "another_test_probe"],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "fqdns": []
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_dns_fails_without_params(self):
        self.create_operation_fails_without_params("dns")

    def test_create_ping_fails_without_params(self):
        self.create_operation_fails_without_params("ping")

    def test_create_traceroute_fails_without_params(self):
        self.create_operation_fails_without_params("traceroute")

    def create_operation_fails_without_params(self, operation):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            f'/{operation}',
            json=dict(
                operation=operation,
                probes=[probes[0]["identifier"]],
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_dns_fails_without_probes(self):
        self.create_operation_fails_without_probes("dns")

    def test_create_ping_fails_without_probes(self):
        self.create_operation_fails_without_probes("ping")

    def test_create_traceroute_fails_without_probes(self):
        self.create_operation_fails_without_probes("traceroute")

    def create_operation_fails_without_probes(self, operation):
        res = self.client.post(
            f'/{operation}',
            json=dict(
                operation=operation,
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"]
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_dns_fails_with_empty_probes(self):
        self.create_operation_fails_with_empty_probes("dns")

    def test_create_ping_fails_with_empty_probes(self):
        self.create_operation_fails_with_empty_probes("ping")

    def test_create_traceroute_fails_with_empty_probes(self):
        self.create_operation_fails_with_empty_probes("traceroute")

    def create_operation_fails_with_empty_probes(self, operation):
        res = self.client.post(
            f'/{operation}',
            json=dict(
                operation=operation,
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"]
                },
                result_format="json",
                probes=[]
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_dns_fails_with_invalid_cron(self):
        self.create_operation_fails_with_invalid_cron("dns")

    def test_create_ping_fails_with_invalid_cron(self):
        self.create_operation_fails_with_invalid_cron("ping")

    def test_create_traceroute_fails_with_invalid_cron(self):
        self.create_operation_fails_with_invalid_cron("traceroute")

    def create_operation_fails_with_invalid_cron(self, operation):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            f'/{operation}',
            json=dict(
                operation=operation,
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "cron": "invalid",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json",
                probes=[probes[0]["identifier"]]
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_traceroute_with_confidence_greater_or_equals_than_one_gets_rejected(self):
        self.create_traceroute_with_confidence(1, 400)

    def test_create_traceroute_with_confidence_lower_than_zero_gets_rejected(self):
        self.create_traceroute_with_confidence(-0.01, 400)

    def test_create_traceroute_with_valid_confidence(self):
        self.create_traceroute_with_confidence(0.99, 201)

    def create_traceroute_with_confidence(self, confidence, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "confidence": confidence,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_traceroute_with_icp_method(self):
        self.create_traceroute_with_method("icp", 201)

    def test_create_traceroute_with_udp_paris_method(self):
        self.create_traceroute_with_method("udp-paris", 201)

    def test_create_traceroute_with_icmp_paris_method(self):
        self.create_traceroute_with_method("icmp-paris", 201)

    def test_create_traceroute_with_invalid_method_gets_rejected(self):
        self.create_traceroute_with_method("thisIsAnInvalidMethod", 400)

    def create_traceroute_with_method(self, method, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "method": method,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_traceroute_with_maxttl_greater_than_255_gets_rejected(self):
        self.create_traceroute_with_maxttl(256, 400)

    def test_create_traceroute_with_maxttl_lower_than_one_gets_rejected(self):
        self.create_traceroute_with_maxttl(0, 400)

    def test_create_traceroute_with_valid_maxttl(self):
        self.create_traceroute_with_maxttl(5, 201)

    def create_traceroute_with_maxttl(self, maxttl, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "maxttl": maxttl,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_traceroute_with_attempts_greater_than_10_gets_rejected(self):
        self.create_traceroute_with_attempts(11, 400)

    def test_create_traceroute_with_attempts_lower_than_one_gets_rejected(self):
        self.create_traceroute_with_attempts(0, 400)

    def test_create_traceroute_with_valid_attempts(self):
        self.create_traceroute_with_attempts(5, 201)

    def create_traceroute_with_attempts(self, attempts, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "attempts": attempts,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_traceroute_with_wait_greater_than_20_gets_rejected(self):
        self.create_traceroute_with_wait(21, 400)

    def test_create_traceroute_with_wait_lower_than_one_gets_rejected(self):
        self.create_traceroute_with_wait(0, 400)

    def test_create_traceroute_with_valid_wait(self):
        self.create_traceroute_with_wait(5, 201)

    def create_traceroute_with_wait(self, wait, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "wait": wait,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_traceroute_with_wait_probe_greater_than_100_gets_rejected(self):
        self.create_traceroute_with_wait_probe(101, 400)

    def test_create_traceroute_with_wait_probe_lower_than_zero_gets_rejected(self):
        self.create_traceroute_with_wait_probe(-1, 400)

    def test_create_traceroute_with_valid_wait_probe(self):
        self.create_traceroute_with_wait_probe(5, 201)

    def create_traceroute_with_wait_probe(self, wait_probe, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "wait-probe": wait_probe,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_traceroute_without_cron(self):
        self.create_traceroute_with_missing_time_param("cron")

    def test_traceroute_without_stop_time(self):
        self.create_traceroute_with_missing_time_param("stop_time")

    def test_traceroute_without_times_per_minute(self):
        self.create_traceroute_with_missing_time_param("times_per_minute")

    def create_traceroute_with_missing_time_param(self, missing_param_name):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        traceroute_params = {
            "ips": [],
            "fqdns": ["www.google.com"],
            "cron": "* * * * *",
            "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "times_per_minute": 1
        }
        del traceroute_params[missing_param_name]
        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"]],
                params=traceroute_params,
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_ping_with_wait_probecount_greater_than_100_gets_rejected(self):
        self.create_ping_with_wait_probe_count(101, 400)

    def test_create_ping_with_wait_probecount_lower_than_one_gets_rejected(self):
        self.create_ping_with_wait_probe_count(0, 400)

    def test_create_ping_with_valid_wait_probecount(self):
        self.create_ping_with_wait_probe_count(5, 201)

    def create_ping_with_wait_probe_count(self, wait_probe_count, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/ping',
            json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "probecount": wait_probe_count,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_ping_with_wait_greater_than_20_gets_rejected(self):
        self.create_ping_with_wait(21, 400)

    def test_create_ping_with_wait_lower_than_one_gets_rejected(self):
        self.create_ping_with_wait(0, 400)

    def test_create_ping_with_valid_wait(self):
        self.create_ping_with_wait(5, 201)

    def create_ping_with_wait(self, wait, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/ping',
            json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "wait": wait,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_ping_without_cron(self):
        self.create_dns_with_missing_timing_param("cron")

    def test_create_ping_without_stop_time(self):
        self.create_dns_with_missing_timing_param("stop_time")

    def test_create_ping_without_times_per_minute(self):
        self.create_dns_with_missing_timing_param("times_per_minute")

    def create_ping_with_missing_timing_param(self, missing_param_name):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        ping_params = {
            "ips": [],
            "fqdns": ["www.google.com"],
            "cron": "* * * * *",
            "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "times_per_minute": 1
        }
        del ping_params[missing_param_name]
        res = self.client.post(
            '/ping',
            json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params=ping_params,
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_ping_with_icmp_echo_method(self):
        self.create_ping_with_method("icmp-echo", 201)

    def test_create_ping_with_icmp_time_method(self):
        self.create_ping_with_method("icmp-time", 201)

    def test_create_ping_with_tcp_syn_method(self):
        self.create_ping_with_method("tcp-syn", 201)

    def test_create_ping_with_tcp_ack_method(self):
        self.create_ping_with_method("tcp-ack", 201)

    def test_create_ping_with_tcp_ack_sport_method(self):
        self.create_ping_with_method("tcp-ack-sport", 201)

    def test_create_ping_with_udp_method(self):
        self.create_ping_with_method("udp", 201)

    def test_create_ping_with_udp_dport_method(self):
        self.create_ping_with_method("udp-dport", 201)

    def test_create_ping_with_invalid_method(self):
        self.create_ping_with_method("thisIsAnInvalidMethod", 400)

    def create_ping_with_method(self, method, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/ping',
            json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "method": method,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_ping_with_size_greater_than_255_gets_rejected(self):
        self.create_ping_with_size(256, 400)

    def test_create_ping_with_size_lower_than_one_gets_rejected(self):
        self.create_ping_with_size(0, 400)

    def test_create_ping_with_valid_size(self):
        self.create_ping_with_size(5, 201)

    def create_ping_with_size(self, size, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/ping',
            json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "size": size,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_ping_with_timeout_greater_than_100_gets_rejected(self):
        self.create_ping_with_timeout(101, 400)

    def test_create_ping_with_timeout_lower_than_zero_gets_rejected(self):
        self.create_ping_with_timeout(-1, 400)

    def test_create_ping_with_valid_timeout(self):
        self.create_ping_with_timeout(5, 201)

    def create_ping_with_timeout(self, timeout, expected_status_code):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/ping',
            json=dict(
                operation="ping",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "timeout": timeout,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(expected_status_code, res.status_code)

    def test_create_dns_with_a_type(self):
        self.create_dns_with_type("a")

    def test_create_dns_with_any_type(self):
        self.create_dns_with_type("any")

    def test_create_dns_with_axfr_type(self):
        self.create_dns_with_type("axfr")

    def test_create_dns_with_hinfo_type(self):
        self.create_dns_with_type("hinfo")

    def test_create_dns_with_mx_type(self):
        self.create_dns_with_type("mx")

    def test_create_dns_with_ns_type(self):
        self.create_dns_with_type("ns")

    def test_create_dns_with_soa_type(self):
        self.create_dns_with_type("soa")

    def test_create_dns_with_txt_type(self):
        self.create_dns_with_type("txt")

    def create_dns_with_type(self, type):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "type": type,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(201, res.status_code)

    def test_create_dns_with_invalid_type(self):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": [],
                    "fqdns": ["www.google.com"],
                    "type": "invalidType",
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_dns_without_cron(self):
        self.create_dns_with_missing_timing_param("cron")

    def test_create_dns_without_stop_time(self):
        self.create_dns_with_missing_timing_param("stop_time")

    def test_create_dns_without_times_per_minute(self):
        self.create_dns_with_missing_timing_param("times_per_minute")

    def create_dns_with_missing_timing_param(self, missing_param_name):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        dns_params = {
            "ips": [],
            "fqdns": ["www.google.com"],
            "cron": "* * * * *",
            "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "times_per_minute": 1
        }
        del dns_params[missing_param_name]
        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=[probes[0]["identifier"]],
                params=dns_params,
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )
        json.loads(res.data)
        self.assertEqual(400, res.status_code)

    def test_create_dns_ips_should_be_empty(self):
        res_probes = self.client.get('/probes')
        probes = json.loads(res_probes.data)
        res = self.client.post(
            '/dns',
            json=dict(
                operation="dns",
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["myIp"],
                    "fqdns": ["www.google.com"],
                    "type": "txt",
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
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
                    "fqdns": ["www.google.com", "www.facebook.com"],
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
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
                    "fqdns": ["www.google.com", "www.facebook.com"],
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )

        self.assertEqual(404, res.status_code)

    def test_creates_traceroute_returns_only_avail_probes(self):
        self.register_probe(self.access_token, self.LOCATION)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/traceroute',
            json=dict(
                operation="traceroute",
                probes=[probes[0]["identifier"], probes[1]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
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
                    "fqdns": ["www.google.com", "www.facebook.com"],
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(data["credits"], 2)

    def test_creates_operation_includes_credits_per_probe(self):
        probe_conn = self.start_connection(self.access_token, self.LOCATION)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/dns',
            json=dict(
                probes=[probes[0]["identifier"], probes[1]["identifier"]],
                params={
                    "fqdns": ["www.google.com", "www.facebook.com"],
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                }
            ),
            headers={'access_token': self.access_token}
        )

        data = json.loads(res.data)

        self.assertEqual(data["credits"], 4)

        probe_conn.disconnect()

    def test_creates_operation_includes_credits_per_probe_available(self):
        self.register_probe(self.access_token, self.LOCATION)

        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/dns',
            json=dict(
                probes=[probes[0]["identifier"], probes[1]["identifier"]],
                params={
                    "fqdns": ["www.google.com", "www.facebook.com"],
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
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
                    ],
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
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
                    "confidence": 0.95,
                    "cron": "* * * * *",
                    "stop_time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )

        user = self.app.db.users.find_user("agustin@gmail.com")

        self.assertEqual(user.credits, 370)

    def test_creates_operation_changes_credits_for_user_counting_operations(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/ping',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "cron": "* * * * *",
                    "stop_time": (datetime.now() + timedelta(minutes=10)).strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )

        user = self.app.db.users.find_user("agustin@gmail.com")

        self.assertEqual(user.credits, 382)

    def test_creates_operation_changes_credits_for_user_counting_times_per_minute(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        res = self.client.post(
            '/ping',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "cron": "* * * * *",
                    "stop_time": (datetime.now() + timedelta(minutes=10)).strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 2
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )

        user = self.app.db.users.find_user("agustin@gmail.com")

        self.assertEqual(user.credits, 364)

    def test_get_all_operations_gets_empty_list_no_operation(self):
        res = self.client.get(
            '/operations',
            headers={'access_token': self.access_token}
        )

        operations = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(operations))

    def test_get_all_operations_invalid_no_auth_token(self):
        res = self.client.get(
            '/operations'
        )

        self.assertEqual(401, res.status_code)

    def test_get_all_operations_success(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        self.client.post(
            '/ping',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "cron": "* * * * *",
                    "stop_time": (datetime.now() + timedelta(minutes=10)).strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )

        res = self.client.get(
            '/operations',
            headers={'access_token': self.access_token}
        )

        operations = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(operations))

    def test_get_all_operations_doesnt_contain_results(self):
        res_probes = self.client.get('/probes')

        probes = json.loads(res_probes.data)

        self.client.post(
            '/ping',
            json=dict(
                probes=[probes[0]["identifier"]],
                params={
                    "ips": ["192.168.0.0", "192.162.1.1"],
                    "cron": "* * * * *",
                    "stop_time": (datetime.now() + timedelta(minutes=10)).strftime("%d/%m/%Y %H:%M"),
                    "times_per_minute": 1
                },
                result_format="json"
            ),
            headers={'access_token': self.access_token}
        )

        res = self.client.get(
            '/operations',
            headers={'access_token': self.access_token}
        )

        operations = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(False, "results" in operations[0])
