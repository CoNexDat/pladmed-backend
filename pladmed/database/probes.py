from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.probe import Probe

class ProbesCollection:
    def __init__(self, db):
        self.db = db
    
    def create_probe(self, user):
        data = {
            "owner": user._id
        }

        _id = self.db.probes.insert_one(data)

        probe = Probe(str(_id.inserted_id))

        return probe
