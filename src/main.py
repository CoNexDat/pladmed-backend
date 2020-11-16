from flask import Flask, make_response, jsonify
from flask_cors import CORS
import os
from db.connection import Database
import logging

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s || %(levelname)s: %(message)s',
    filename='logs/' + os.getenv('LOG_FILE', 'default_logs'),
    level=logging.DEBUG
)

mongo_user = os.getenv('MONGO_USERNAME', '')
mongo_password = os.getenv('MONGO_PASSWORD', '')
mongo_host = os.getenv('MONGO_HOST', 'localhost')
mongo_port = os.getenv('MONGO_PORT', "27017")
mongo_db = os.getenv('MONGO_DATABASE', 'pladmed')

db = Database(mongo_user, mongo_password, mongo_host, mongo_port, mongo_db)

CORS(app)

@app.route('/')
def root():
    try:
        db.save_user("juan@gmail.com", "password")
        user = db.find_user("juan@gmail.com")

        return make_response(
            jsonify(
                id=40,
                email=user["email"]
            ),
            200
        )
    except Exception as e:
        print("Failed mongodb: ", e)
        return make_response(
            jsonify(
                error="Error in database"
            ),
            404
        )    


if __name__ == "__main__":
    debug = int(os.getenv("DEBUG", True))

    port = int(os.getenv("PORT", 5000))

    app.run(host='0.0.0.0', port=port, debug=debug)
