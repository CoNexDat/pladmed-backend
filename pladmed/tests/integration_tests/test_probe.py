import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json
from pladmed import socketio
from unittest import mock
import pladmed.routes.events as events
import pladmed.routes.routes as routes


class ProbeBaseTest(BaseTest):
    def test_get_all_probes_zero_if_not_created(self):
        res = self.client.get(
            '/probes'
        )

        data = json.loads(res.data)

        self.assertEqual(len(data), 0)

    def test_connection_refuse_no_token(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client,
            headers={"total_credits": 130, "in_use_credits": 0}
        )

        self.assertEqual(len(self.app.probes), 0)

    def test_connection_refuse_invalid_token(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string="token=fake_token",
            headers={"total_credits": 130, "in_use_credits": 0}
        )

        self.assertEqual(len(self.app.probes), 0)

    def test_connection_refuse_fake_token(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string="token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiNWZkODkwZWIxOTIxMGUxODg0ZWU5NDRmIn0.lcyp89G7GobSTe8qQnCNmDKNFFl1jRtyAWymlWJWpa4",
            headers={"total_credits": 130, "in_use_credits": 0}
        )

        self.assertEqual(len(self.app.probes), 0)

    def test_connection_refuse_fake_token_key(self):
        probe = socketio.test_client(
            self.app,
            flask_test_client=self.client,
            query_string="token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1ZmQ4NGE1YzY5NzkxYWVkNWNhNjUzYzMiLCJlbWFpbCI6ImZlZGUuZnVuZXM5NkBnbWFpbC5jb20ifQ.72LNISUUAwBO_dLpAJXtLM9Nsco1FuUYTdDiSzvB_Qs",
            headers={"total_credits": 130, "in_use_credits": 0}
        )

        self.assertEqual(len(self.app.probes), 0)


class ProbeTest(BaseTest):
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

    def test_connection_up(self):
        self.assertEqual(len(self.app.probes), 1)

    def test_disconnect(self):
        self.probe_conn.disconnect()

        self.assertEqual(len(self.app.probes), 0)

    def test_receives_traceroute(self):
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
            headers={'access_token': self.access_token}
        )

        received = self.probe_conn.get_received()

        self.assertEqual(received[0]["name"], "traceroute")
        self.assertEqual(received[0]["args"][0]
                         ["params"]["ips"][0], "192.168.0.0")

    def test_receives_ping(self):
        res = self.client.get('/probes')

        probes = json.loads(res.data)

        self.client.post('/ping', json=dict(
            operation="ping",
            probes=[probes[0]["identifier"]],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"]
            }
        ),
            headers={'access_token': self.access_token}
        )

        received = self.probe_conn.get_received()

        self.assertEqual(received[0]["name"], "ping")
        self.assertEqual(received[0]["args"][0]
                         ["params"]["ips"][0], "192.168.0.0")

    def test_receives_dns(self):
        res = self.client.get('/probes')

        probes = json.loads(res.data)

        self.client.post('/dns', json=dict(
            operation="dns",
            probes=[probes[0]["identifier"]],
            params={
                "domains": ["www.google.com", "www.facebook.com"]
            }
        ),
            headers={'access_token': self.access_token}
        )

        received = self.probe_conn.get_received()

        self.assertEqual(received[0]["name"], "dns")
        self.assertEqual(received[0]["args"][0]
                         ["params"]["domains"][0], "www.google.com")

    def test_send_operation_results(self):
        res = self.client.get('/probes')

        probes = json.loads(res.data)

        res = self.client.post('/traceroute', json=dict(
            operation="traceroute",
            probes=[probes[0]["identifier"]],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ),
            headers={'access_token': self.access_token}
        )

        # Discard traceroute received, let's mock the client
        received = self.probe_conn.get_received()

        operation_id = json.loads(res.data)["_id"]

        with open("pladmed/tests/tests_files/warts_example", 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation_id,
                "content": content,
                "unique_code": "an unique code",
                "format": "warts"
            }

            ack = self.probe_conn.emit(
                "results",
                data_to_send,
                callback=True
            )

            self.assertEqual(ack, operation_id)

    def test_send_operation_results_updates_results(self):
        res = self.client.get('/probes')

        probes = json.loads(res.data)

        res = self.client.post('/traceroute', json=dict(
            operation="traceroute",
            probes=[probes[0]["identifier"]],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ),
            headers={'access_token': self.access_token}
        )

        # Discard traceroute received, let's mock the client
        received = self.probe_conn.get_received()

        operation_id = json.loads(res.data)["_id"]

        with open("pladmed/tests/tests_files/warts_example", 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation_id,
                "content": content,
                "unique_code": "an unique code",
                "format": "warts"
            }

            self.probe_conn.emit(
                "results",
                data_to_send,
                callback=True
            )

        operation = self.app.db.operations.find_operation(operation_id)

        self.assertEqual(operation.results[0]
                         ["probe"], probes[0]["identifier"])

    def test_send_operation_results_fails_if_probe_suddenly_disconnects(self):
        mock_probe_conn = mock.patch.object(
            events, 'find_probe_by_session', return_value=None
        )

        res = self.client.get('/probes')

        probes = json.loads(res.data)

        res = self.client.post('/traceroute', json=dict(
            operation="traceroute",
            probes=[probes[0]["identifier"]],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ),
            headers={'access_token': self.access_token}
        )

        # Discard traceroute received, let's mock the client
        received = self.probe_conn.get_received()

        operation_id = json.loads(res.data)["_id"]

        with open("pladmed/tests/tests_files/warts_example", 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation_id,
                "content": content,
                "unique_code": "an unique code",
                "format": "warts"
            }

            with mock_probe_conn:
                res = self.probe_conn.emit(
                    "results",
                    data_to_send,
                    callback=True
                )

                self.assertEqual([], res)

    def test_send_operation_results_rejects_duplicates(self):
        res = self.client.get('/probes')

        probes = json.loads(res.data)

        res = self.client.post('/traceroute', json=dict(
            operation="traceroute",
            probes=[probes[0]["identifier"]],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ),
            headers={'access_token': self.access_token}
        )

        # Discard traceroute received, let's mock the client
        received = self.probe_conn.get_received()

        operation_id = json.loads(res.data)["_id"]

        with open("pladmed/tests/tests_files/warts_example", 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation_id,
                "content": content,
                "unique_code": "an unique code",
                "format": "warts"
            }

            self.probe_conn.emit(
                "results",
                data_to_send,
                callback=True
            )

            data_to_send = {
                "operation_id": operation_id,
                "content": content,
                "unique_code": "an unique code",
                "format": "warts"
            }

            ack = self.probe_conn.emit(
                "results",
                data_to_send,
                callback=True
            )

            operation = self.app.db.operations.find_operation(operation_id)

            self.assertEqual(len(operation.results), 1)
            self.assertEqual(ack, operation_id)

    def test_connection_sets_max_credits(self):
        self.assertEqual(list(self.app.probes.values())[0].total_credits, 40)

    def test_connection_sets_in_use_credits(self):
        self.assertEqual(list(self.app.probes.values())[0].in_use_credits, 0)

    def test_probe_updates_when_new_operation(self):
        data_to_send = {
            "credits": 30
        }

        self.probe_conn.emit(
            "new_operation",
            data_to_send
        )

        self.assertEqual(list(self.app.probes.values())[0].in_use_credits, 30)

    def test_probe_updates_when_new_operation_doesnt_change_other_probe(self):
        data_to_send = {
            "credits": 30
        }

        self.start_connection(self.access_token)

        self.probe_conn.emit(
            "new_operation",
            data_to_send
        )

        conns = list(self.app.probes.values())

        self.assertEqual(conns[1].in_use_credits, 0)

    def test_probe_updates_when_finish_operation(self):
        data_to_send = {
            "credits": 30
        }

        self.probe_conn.emit(
            "new_operation",
            data_to_send
        )

        data_to_send = {
            "credits": 30
        }

        self.probe_conn.emit(
            "finish_operation",
            data_to_send
        )
        conns = list(self.app.probes.values())

        self.assertEqual(conns[0].in_use_credits, 0)

    def test_send_operation_results_gives_owner_credits(self):
        res = self.client.get('/probes')

        probes = json.loads(res.data)

        res = self.client.post('/traceroute', json=dict(
            operation="traceroute",
            probes=[probes[0]["identifier"]],
            params={
                "ips": ["192.168.0.0", "192.162.1.1"],
                "confidence": 0.95
            }
        ),
            headers={'access_token': self.access_token}
        )

        # Discard traceroute received, let's mock the client
        received = self.probe_conn.get_received()

        operation_id = json.loads(res.data)["_id"]

        with open("pladmed/tests/tests_files/warts_example", 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation_id,
                "content": content,
                "unique_code": "an unique code",
                "format": "warts"
            }

            self.probe_conn.emit(
                "results",
                data_to_send,
                callback=True
            )

        user = self.app.db.users.find_user("agustin@gmail.com")

        self.assertEqual(user.credits, 380)

    # ---------------------------------------------
    # API Rest test
    # ---------------------------------------------

    def test_register_probe_correctly(self):
        res = self.client.post(
            '/probes',
            headers={'access_token': self.access_token}
        )

        self.assertEqual(res.status_code, 201)

    def test_register_probe_doesnt_work_without_token(self):
        res = self.client.post('/probes')

        self.assertEqual(res.status_code, 401)

    def test_register_probe_doesnt_work_without_invalid_token(self):
        res = self.client.post(
            '/probes',
            headers={'access_token': "fake_token"}
        )

        self.assertEqual(res.status_code, 401)

    def test_register_probe_correctly_gets_token(self):
        self.assertEqual(len(self.access_token) > 0, True)

    def test_get_all_probes(self):
        res = self.client.get(
            '/probes'
        )

        data = json.loads(res.data)

        self.assertEqual(len(data), 1)
