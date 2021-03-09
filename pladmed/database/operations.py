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
    
    def create_operation(self, operation, params, probes, user, credits_, format_):
        data = {
            "operation": operation,
            "params": params,
            "probes": [ObjectId(probe.identifier) for probe in probes],
            "owner": ObjectId(user._id),
            "credits": credits_,
            "result_format": format_
        }

        _id = self.operationsCol.insert_one(data)

        op = Operation(
            str(_id.inserted_id),
            operation,
            params,
            probes,
            credits_,
            format_
        )

        return op

    def find_operation(self, identifier):
        try:
            op = self.operationsCol.find_one({"_id": ObjectId(identifier)})

            operation = Operation(
                str(op["_id"]),
                op["operation"],
                op["params"],
                [Probe(str(probe), str(op["owner"])) for probe in op["probes"]],
                op["credits"],
                op["result_format"]
            )

            if "results" in op:
                for result in op["results"]:
                    operation.add_results(
                        str(result["probe"]),
                        result["results"],
                        result["unique_code"]
                    )

            return operation
        except:
            raise InvalidOperation()

    def add_results(self, operation, probe, results, unique_code):
        new_results = {
            "probe": ObjectId(probe.identifier),
            "results": results,
            "unique_code": unique_code
        }

        self.operationsCol.update_one(
            {"_id": ObjectId(operation._id)},
            {"$push": {"results": new_results}}
        )

        operation.add_results(probe.identifier, results, unique_code)

        return operation
