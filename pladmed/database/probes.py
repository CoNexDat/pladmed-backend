from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.probe import Probe
from bson.objectid import ObjectId
from pladmed.exceptions import InvalidProbe

class ProbesCollection:
    def __init__(self, db):
        self.probesCol = db.probes
    
    def create_probe(self, user):
        data = {
            "owner": ObjectId(user._id)
        }

        _id = self.probesCol.insert_one(data)

        probe = Probe(str(_id.inserted_id))

        return probe

    def find_probe(self, identifier):
        try:
            probe = self.probesCol.find_one({"_id": ObjectId(identifier)})

            return Probe(str(probe["_id"]))
        except:
            return None

    def find_all_probes(self):
        probes = []

        for probe in self.probesCol.find():
            probes.append(Probe(str(probe["_id"])))
            
        return probes

    def find_selected_probes(self, identifiers):
        probes = []

        try:
            probes_ids = [ObjectId(probe) for probe in identifiers]
        except:
            raise InvalidProbe()

        for probe in self.probesCol.find({ "_id": { "$in": probes_ids } }):
            probes.append(Probe(str(probe["_id"])))

        if len(probes_ids) != len(probes):
            raise InvalidProbe()
                
        return probes
