from pymongo import MongoClient
import urllib.parse
import logging

class UsersCollection:
    def __init__(self, db):
        self.db = db
        self.db.users.create_index("email", unique=True)
    
    def save_user(self, user):
        self.db.users.insert_one(user.__dict__)

    def find_user(self, email):
        return self.db.users.find_one({"email": email})
