from pymongo import MongoClient
import urllib.parse
import logging

class Database:
    def __init__(self, username, password, host, port, db):
        logging.info(
            "Connecting to: " +
            'mongodb://' +
            urllib.parse.quote_plus(username) +
            ':' +
            urllib.parse.quote_plus(password) +
            '@' +
            host +
            ":" +
            port +
            "/" +
            db        
        )

        self.client = MongoClient(
            'mongodb://' +
            urllib.parse.quote_plus(username) +
            ':' +
            urllib.parse.quote_plus(password) +
            '@' +
            host +
            ":" +
            port +
            "/"
        )

        self.db_name = db
        self.db = self.client[db]

    def save_user(self, email, password):
        user = {
            "email": email,
            "password": password
        }

        self.db.users.insert_one(user)

    def find_user(self, email):
        return self.db.users.find_one({"email": email})

    def reset_db(self):
        self.client.drop_database(self.db_name)
