import unittest
from pladmed.models.operation import Operation
from pladmed.models.probe import Probe
from pladmed.utils.encoders import JsonEncoder
import json

class EncodersTest(unittest.TestCase):
    def test_encodes_dict(self):
        a = {
            "a": 1,
            "b": 2
        }

        b = json.dumps(a, cls=JsonEncoder)

        c = json.loads(b)

        self.assertEqual(len(set(a.keys()) - set(c.keys())), 0)

    def test_encodes_probes(self):
        probe_a = Probe("fake_id")
        probe_b = Probe("another_fake_id")

        probes = [probe_a, probe_b]

        b = json.dumps(probes, cls=JsonEncoder)

        c = json.loads(b)

        self.assertEqual(c[0]["identifier"], "fake_id")

    def test_encodes_single_probe(self):
        probe_a = Probe("fake_id")

        b = json.dumps(probe_a, cls=JsonEncoder)

        c = json.loads(b)

        self.assertEqual(c["identifier"], "fake_id")
