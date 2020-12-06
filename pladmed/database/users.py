from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.user import User

class UsersCollection:
    def __init__(self, db):
        self.db = db
        self.db.users.create_index("email", unique=True)
    
    def create_user(self, email, password):
        _id = self.db.users.insert_one({
            "email": email,
            "password": password
        })

        return User(str(_id.inserted_id), email, password)

    def find_user(self, email):
        return self.db.users.find_one({"email": email})
