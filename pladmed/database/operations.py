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
            "probes": probes,
            "owner": ObjectId(user._id)
        }

        _id = self.db.operations.insert_one(data)

        probe = Operation(
            str(_id.inserted_id),
            operation,
            params,
            probes
        )

        return probe
