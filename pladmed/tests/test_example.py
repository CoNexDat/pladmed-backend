import unittest
from pladmed.tests.test_base import BaseTest
import json

class ExampleTest(BaseTest):
    def test_root(self):
        res = self.client.get('/')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)

    def test_root_fields(self):
        res = self.client.get('/')
        data = json.loads(res.data)
        
        self.assertEqual("juan@gmail.com", data["email"])
        self.assertEqual(40, data["id"])
