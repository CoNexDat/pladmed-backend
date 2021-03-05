import unittest
from pladmed.models.probe import Probe

class ProbeTest(unittest.TestCase):
    def setUp(self):
        self.probe = Probe(
            identifier="3ap394c"
        )

        self.probe.total_credits = 130
        self.probe.in_use_credits = 0

    def test_probe_includes_identifier(self):
        self.assertEqual("3ap394c", self.probe.identifier)

    def test_probe_has_public_data(self):
        self.assertEqual("identifier" in self.probe.public_data(), True)

    def test_probe_includes_total_credits(self):
        self.assertEqual(130, self.probe.total_credits)

    def test_probe_public_data_doesnt_include_total_credits(self):
        self.assertEqual("total_credits" in self.probe.public_data(), False)

    def test_probe_includes_in_use_credits(self):
        self.assertEqual(0, self.probe.in_use_credits)

    def test_probe_public_data_doesnt_include_in_use_credits(self):
        self.assertEqual("in_use_credits" in self.probe.public_data(), False)
