from pymongo import MongoClient
import urllib.parse
import logging

class UsersCollection:
    def __init__(self, db):
        self.db = db
    
    def save_user(self, email, password):
        user = {
            "email": email,
            "password": password
        }

        self.db.users.insert_one(user)

    def find_user(self, email):
        return self.db.users.find_one({"email": email})
