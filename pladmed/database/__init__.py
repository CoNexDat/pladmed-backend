from pymongo import MongoClient
import urllib.parse
import logging
from pladmed.database.users import UsersCollection
from pladmed.database.probes import ProbesCollection

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

        self.init_users()
        self.init_probes()

    # Initialize users collection
    def init_users(self):
        self.users = UsersCollection(self.db)

    # Initialize probes collection
    def init_probes(self):
        self.probes = ProbesCollection(self.db)
    
    def reset_db(self):
        self.client.drop_database(self.db_name)
