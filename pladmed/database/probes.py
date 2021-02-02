from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.probe import Probe
from bson.objectid import ObjectId
from pladmed.exceptions import InvalidProbe

class ProbesCollection:
    def __init__(self, db):
        self.db = db
    
    def create_probe(self, user):
        data = {
            "owner": ObjectId(user._id)
        }

        _id = self.db.probes.insert_one(data)

        probe = Probe(str(_id.inserted_id))

        return probe

    def find_probe(self, identifier):
        try:
            probe = self.db.probes.find_one({"_id": ObjectId(identifier)})

            if not probe:
                return None

            return Probe(str(probe["_id"]))
        except:
            return None

    def find_all_probes(self):
        probes = []

        for probe in self.db.probes.find():
            probes.append(Probe(str(probe["_id"])))
            
        return probes

    def find_selected_probes(self, identifiers):
        probes = []

        try:
            probes_ids = [ObjectId(probe) for probe in identifiers]
        except:
            raise InvalidProbe()

        for probe_id in self.db.probes.find({ "_id": { "$in": probes_ids } }):
            probes.append(self.find_probe(probe_id))

        if len(probes_ids) != len(probes):
            raise InvalidProbe()
                
        return probes
