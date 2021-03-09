import unittest
from pladmed.models.probe import Probe

class ProbeTest(unittest.TestCase):
    def setUp(self):
        self.probe = Probe(
            identifier="3ap394c",
            owner_id=4
        )

    def test_probe_includes_identifier(self):
        self.assertEqual("3ap394c", self.probe.identifier)

    def test_probe_has_public_data(self):
        self.assertEqual("identifier" in self.probe.public_data(), True)

    def test_probe_includes_owner(self):
        self.assertEqual(self.probe.owner_id, 4)
