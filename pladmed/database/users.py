from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.models.user import User
from passlib.hash import pbkdf2_sha256 as secure_password

class UsersCollection:
    def __init__(self, db):
        self.db = db
        self.db.users.create_index("email", unique=True)
    
    def create_user(self, email, password):
        hashed_password = secure_password.hash(password)

        _id = self.db.users.insert_one({
            "email": email,
            "password": hashed_password
        })

        return User(str(_id.inserted_id), email, hashed_password)

    def find_user(self, email):
        user_data = self.db.users.find_one({"email": email})

        if not user_data:
            return None

        return User(
            str(user_data["_id"]),
            user_data["email"],
            user_data["password"]
        )
