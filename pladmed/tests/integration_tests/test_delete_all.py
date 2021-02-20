import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json
from unittest import mock
import os

class DeleteAllTest(BaseTest):
    def test_deletes_everything(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        res = self.client.delete(
            '/delete_all'
        )

        self.assertEqual(res.status_code, 204)
        self.assertEqual(self.app.db.users.usersCol.count_documents({}), 0)

    def test_deletes_everything_doesnt_work_production(self):
        self.app.config.update({"ENV": "production"})

        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_password"
        ))

        res = self.client.delete(
            '/delete_all'
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(self.app.db.users.usersCol.count_documents({}), 1)
