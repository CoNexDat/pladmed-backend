import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
from pladmed.models.user import User
import json

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
