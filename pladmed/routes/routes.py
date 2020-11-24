from flask import current_app, make_response, jsonify
from . import api

@api.route('/')
def root():
    current_app.db.save_user("juan@gmail.com", "password")
    user = current_app.db.find_user("juan@gmail.com")

    return make_response(
        jsonify(
            id=40,
            email=user["email"]
        ),
        200
    )
