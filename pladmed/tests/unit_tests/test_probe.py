import unittest
from pladmed.models.probe import Probe

class ProbeTest(unittest.TestCase):
    def setUp(self):
        self.probe = Probe(
            identifier="3ap394c"
        )

    def test_probe_includes_identifier(self):
        self.assertEqual("3ap394c", self.probe.identifier)
