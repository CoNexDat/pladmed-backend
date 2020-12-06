from flask import current_app, make_response, jsonify, request
from pladmed.routes import api
from flask_socketio import emit
from pladmed.models.user import User

@api.route('/operation', methods=["POST"])
def create_operation():
    data = request.get_json(force=True)

    # TODO Validate data and params

    # TODO Save operation in db

    for conn, probe in list(current_app.probes.items()):
        if probe.identifier in data["probes"]:
            emit(data["operation"], data, room=conn, namespace='')

    return make_response(data, 201)

@api.route('/register', methods=["POST"])
def create_user():
    data = request.get_json(force=True)

    # TODO Validate data and params

    user = User(data["email"], data["password"])

    try:
        current_app.db.users.save_user(user)
    except:
        return make_response({"Error": "That email is already registered"}, 404)

    del data["password"]

    return make_response(data, 201)
