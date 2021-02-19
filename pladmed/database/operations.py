from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.operation import Operation
from pladmed.models.probe import Probe
from bson.objectid import ObjectId
from pladmed.exceptions import InvalidOperation

class OperationsCollection:
    def __init__(self, db):
        self.operationsCol = db.operations
    
    def create_operation(self, operation, params, probes, user):
        data = {
            "operation": operation,
            "params": params,
            "probes": [ObjectId(probe.identifier) for probe in probes],
            "owner": ObjectId(user._id)
        }

        _id = self.operationsCol.insert_one(data)

        op = Operation(
            str(_id.inserted_id),
            operation,
            params,
            probes
        )

        return op

    def find_operation(self, identifier):
        try:
            op = self.operationsCol.find_one({"_id": ObjectId(identifier)})

            operation = Operation(
                str(op["_id"]),
                op["operation"],
                op["params"],
                [Probe(str(probe)) for probe in op["probes"]]
            )

            if "results" in op:
                for result in op["results"]:
                    operation.add_results(Probe(str(result["probe"])), result["results"])

            return operation
        except:
            raise InvalidOperation()

    def add_results(self, operation, probe, results):
        new_results = {
            "probe": ObjectId(probe.identifier),
            "results": results
        }

        self.operationsCol.update_one(
            {"_id": ObjectId(operation._id)},
            {"$push": {"results": new_results}}
        )

        operation.add_results(probe, results)

        return operation
