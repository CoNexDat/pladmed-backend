from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.user import User

class UsersCollection:
    def __init__(self, db):
        self.usersCol = db.users
        self.usersCol.create_index("email", unique=True)
    
    def create_user(self, email, password):
        user = User({"email": email})

        user.set_password(password)

        _id = self.usersCol.insert_one(user.__dict__)

        user._id = str(_id.inserted_id)

        return user

    def find_user(self, email):
        user_data = self.usersCol.find_one({"email": email})

        if not user_data:
            return None

        return User({
            "_id": str(user_data["_id"]),
            "email": user_data["email"],
            "password": user_data["password"]
        })
