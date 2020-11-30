import unittest
from pladmed.models.operation import Operation
from pladmed.models.probe import Probe

class OperationTest(unittest.TestCase):
    def setUp(self):
        self.operation = Operation(
            operation="Traceroute",
            probes=[
                Probe("39232d2"),
                Probe("43i4iec")
            ]
        )

    def test_operation_includes_probes(self):
        self.assertEqual(len(self.operation.probes), 2)

    def test_operation_includes_operation(self):
        self.assertEqual(self.operation.operation, "Traceroute")
