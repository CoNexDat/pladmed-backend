import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
from pladmed.models.user import User
import json
from pladmed.exceptions import InvalidOperation, InvalidProbe

class DatabaseTest(BaseTest):
    def test_creates_users(self):
        user = self.app.db.users.create_user("juan@gmail.com", "123")

        self.assertEqual(user.email, "juan@gmail.com")

    def test_gets_no_user_if_not_created(self):
        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertEqual(user, None)

    def test_find_users(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertEqual(user.email, "juan@gmail.com")        

    def test_reset_db(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        self.app.db.reset_db()

        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertEqual(user, None)

    def test_password_is_secure(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.assertNotEqual(user.password, "123")
        self.assertEqual(user.verify_password("123"), True)

    def test_creates_probes(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        probe = self.app.db.probes.create_probe(user)

        self.assertEqual(hasattr(probe, "identifier"), True)

    def test_find_probe(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        probe = self.app.db.probes.create_probe(user)

        ret_probe = self.app.db.probes.find_probe(probe.identifier)

        self.assertEqual(probe.identifier, ret_probe.identifier)

    def test_find_probe_invalid_id(self):
        probe = self.app.db.probes.find_probe("fake_identifier")

        self.assertEqual(probe, None)

    def test_find_probe_no_exists(self):
        probe = self.app.db.probes.find_probe("5fd88dcaa1fe1d28abe9e154")

        self.assertEqual(probe, None)        

    def test_find_all_probes(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.app.db.probes.create_probe(user)
        self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_all_probes()

        self.assertEqual(len(probes), 2)

    def test_find_all_probes_no_exist(self):
        probes = self.app.db.probes.find_all_probes()

        self.assertEqual(len(probes), 0)

    def test_creates_operation(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.app.db.probes.create_probe(user)
        self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_all_probes()

        operation = "traceroute"

        params = {
            "confidence": 0.95,
            "ips": ["192.168.0.0", "192.168.0.1"]
        }

        credits_ = 10

        op = self.app.db.operations.create_operation(
            operation,
            params,
            probes,
            user,
            credits_
        )

        self.assertEqual(hasattr(op, "params"), True)

    def test_find_operation(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.app.db.probes.create_probe(user)
        self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_all_probes()

        operation = "traceroute"

        params = {
            "confidence": 0.95,
            "ips": ["192.168.0.0", "192.168.0.1"]
        }

        credits_ = 10

        op = self.app.db.operations.create_operation(
            operation,
            params,
            probes,
            user,
            credits_
        )

        same_op = self.app.db.operations.find_operation(op._id)

        self.assertEqual(same_op._id, op._id)

    def test_find_operation_no_exists(self):
        with self.assertRaises(InvalidOperation):
            self.app.db.operations.find_operation("operation_fake")

    def test_find_selected_probes(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        probe_1 = self.app.db.probes.create_probe(user)
        probe_2 = self.app.db.probes.create_probe(user)
        probe_3 = self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_selected_probes(
            [probe_1.identifier, probe_2.identifier]
        )

        self.assertEqual(len(probes), 2)

    def test_find_selected_probes_raises_invalid_probe(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        probe_1 = self.app.db.probes.create_probe(user)

        with self.assertRaises(InvalidProbe):
            self.app.db.probes.find_selected_probes(
                [probe_1.identifier, "5fd93938d1af6852c13aae23"]
            )

    def test_find_selected_probes_raises_fake_probe(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        probe_1 = self.app.db.probes.create_probe(user)

        with self.assertRaises(InvalidProbe):
            self.app.db.probes.find_selected_probes(
                [probe_1.identifier, "1451515"]
            )

    def test_add_results_to_operation(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.app.db.probes.create_probe(user)
        self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_all_probes()

        operation = "traceroute"

        params = {
            "confidence": 0.95,
            "ips": ["192.168.0.0", "192.168.0.1"]
        }

        credits_ = 10

        op = self.app.db.operations.create_operation(
            operation,
            params,
            probes,
            user,
            credits_
        )

        results = "Traceroute results..."
        unique_code = "an unique code"

        updated_op = self.app.db.operations.add_results(
            op,
            probes[0],
            results,
            unique_code
        )

        self.assertEqual(updated_op._id, op._id)
        self.assertEqual(updated_op.results[0]["probe"], probes[0])
        self.assertEqual(updated_op.results[0]["results"], results)

    def test_find_operation_includes_results(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.app.db.probes.create_probe(user)
        self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_all_probes()

        operation = "traceroute"

        params = {
            "confidence": 0.95,
            "ips": ["192.168.0.0", "192.168.0.1"]
        }

        credits_ = 10

        op = self.app.db.operations.create_operation(
            operation,
            params,
            probes,
            user,
            credits_
        )

        results = "Traceroute results..."
        unique_code = "an unique code"

        updated_op = self.app.db.operations.add_results(
            op,
            probes[0],
            results,
            unique_code
        )

        same_op = self.app.db.operations.find_operation(op._id)

        self.assertEqual(same_op.results[0]["probe"], probes[0])
        self.assertEqual(same_op.results[0]["results"], results)

    def test_creates_operation_includes_credits(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.app.db.probes.create_probe(user)
        self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_all_probes()

        operation = "traceroute"

        params = {
            "confidence": 0.95,
            "ips": ["192.168.0.0", "192.168.0.1"]
        }

        credits_ = 10

        op = self.app.db.operations.create_operation(
            operation,
            params,
            probes,
            user,
            credits_
        )

        self.assertEqual(op.credits, 10)

    def test_find_operation_includes_credits(self):
        self.app.db.users.create_user("juan@gmail.com", "123")

        user = self.app.db.users.find_user("juan@gmail.com")

        self.app.db.probes.create_probe(user)
        self.app.db.probes.create_probe(user)

        probes = self.app.db.probes.find_all_probes()

        operation = "traceroute"

        params = {
            "confidence": 0.95,
            "ips": ["192.168.0.0", "192.168.0.1"]
        }

        credits_ = 10

        op = self.app.db.operations.create_operation(
            operation,
            params,
            probes,
            user,
            credits_
        )

        same_op = self.app.db.operations.find_operation(op._id)

        self.assertEqual(same_op.credits, op.credits)

    def test_user_created_has_no_credits(self):
        user = self.app.db.users.create_user("juan@gmail.com", "123")

        self.assertEqual(user.credits, 0)

    def test_updates_user_credits(self):
        user = self.app.db.users.create_user("juan@gmail.com", "123")

        user_upd = self.app.db.users.change_credits(user, 30)

        self.assertEqual(user_upd.credits, 30)
