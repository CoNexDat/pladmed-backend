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

            return self.deserialize_operation(op)
        except:
            raise InvalidOperation()

    def find_by_user(self, user_id):
        operations = []

        user_query = {"owner": ObjectId(user_id)}

        for op in self.operationsCol.find(user_query):
            operation = self.deserialize_operation(op)
            operations.append(operation)

        return operations

    def deserialize_operation(self, raw_operation):
        operation = Operation(
            str(raw_operation["_id"]),
            raw_operation["operation"],
            raw_operation["params"],
            [Probe(str(probe), str(raw_operation["owner"]), None)
                for probe in raw_operation["probes"]],
            raw_operation["credits"],
            raw_operation["result_format"]
        )

        if "results" in raw_operation:
            for result in raw_operation["results"]:
                operation.add_results(
                    str(result["probe"]),
                    result["results"],
                    result["unique_code"]
                )

        return operation

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
