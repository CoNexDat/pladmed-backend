import unittest
from pladmed.models.operation import Operation
from pladmed.models.probe import Probe

class OperationTest(unittest.TestCase):
    def setUp(self):
        self.operation = Operation(
            _id="operation_id",
            operation="Traceroute",
            params={
                "ips": ["192.168.0.0", "192.168.0.1"],
                "confidence": 0.95,

            },
            probes=[
                Probe("39232d2"),
                Probe("43i4iec")
            ]
        )

    def test_operation_includes_probes(self):
        self.assertEqual(len(self.operation.probes), 2)

    def test_operation_includes_operation(self):
        self.assertEqual(self.operation.operation, "Traceroute")

    def test_operation_includes_params(self):
        self.assertEqual(self.operation.params["confidence"], 0.95)

    def test_operation_includes_id(self):
        self.assertEqual(self.operation._id, "operation_id")

    def test_operation_has_public_data(self):
        self.assertEqual("_id" in self.operation.public_data(), True)

    def test_operation_includes_results(self):
        self.assertEqual(len(self.operation.results), 0)
