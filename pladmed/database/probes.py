from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.probe import Probe
from bson.objectid import ObjectId
from pladmed.exceptions import InvalidProbe


class ProbesCollection:
    def __init__(self, db):
        self.usersCol = db.users
        self.probesCol = db.probes

    def create_probe(self, user, location):
        data = {
            "owner": ObjectId(user._id),
            "location": self.to_geo_json(location)
        }

        _id = self.probesCol.insert_one(data)

        probe = Probe(str(_id.inserted_id), user._id, location)

        return probe

    def to_geo_json(self, location):
        return {
            "coordinates": [location["longitude"], location["latitude"]],
            "type": "Point"
        }

    def find_probe(self, identifier):
        try:
            probe = self.probesCol.find_one({"_id": ObjectId(identifier)})
            location = self.from_geo_json(probe["location"])

            return Probe(str(probe["_id"]), str(probe["owner"]), location)
        except:
            return None

    def from_geo_json(self, geo_json):
        return {
            "longitude": geo_json["coordinates"][0],
            "latitude": geo_json["coordinates"][1]
        }

    def find_all_probes(self):
        probes = []

        for probe in self.probesCol.find():
            location = self.from_geo_json(probe["location"])
            probes.append(
                Probe(str(probe["_id"]), str(probe["owner"]), location))

        return probes

    def find_selected_probes(self, identifiers):
        probes = []

        try:
            probes_ids = [ObjectId(probe) for probe in identifiers]
        except:
            raise InvalidProbe()

        for probe in self.probesCol.find({"_id": {"$in": probes_ids}}):
            location = self.from_geo_json(probe["location"])
            probes.append(
                Probe(str(probe["_id"]), str(probe["owner"]), location))

        if len(probes_ids) != len(probes):
            raise InvalidProbe()

        return probes
