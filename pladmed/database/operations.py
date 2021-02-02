from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.operation import Operation
from bson.objectid import ObjectId

class OperationsCollection:
    def __init__(self, db):
        self.db = db
    
    def create_operation(self, operation, params, probes, user):
        data = {
            "operation": operation,
            "params": params,
            "probes": [ObjectId(probe) for probe in probes],
            "owner": ObjectId(user._id)
        }

        _id = self.db.operations.insert_one(data)

        operation = Operation(
            str(_id.inserted_id),
            operation,
            params,
            probes
        )

        return operation

    def find_operation(self, identifier):
        try:
            op = self.db.operations.find_one({"_id": ObjectId(identifier)})

            if not op:
                return None

            return Operation(
                str(op["_id"]),
                op["operation"],
                op["params"],
                op["probes"]
            )
        except:
            return None
