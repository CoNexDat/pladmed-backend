from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.user import User

class UsersCollection:
    def __init__(self, db):
        self.db = db
        self.db.users.create_index("email", unique=True)
    
    def create_user(self, email, password):
        user = User({"email": email, "raw_password": password})

        _id = self.db.users.insert_one(user.__dict__)

        user._id = str(_id.inserted_id)

        return user

    def find_user(self, email):
        user_data = self.db.users.find_one({"email": email})

        if not user_data:
            return None

        return User({
            "_id": str(user_data["_id"]),
            "email": user_data["email"],
            "password": user_data["password"]
        })
