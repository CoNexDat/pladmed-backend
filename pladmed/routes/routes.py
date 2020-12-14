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

    try:
        user = current_app.db.users.create_user(
            data["email"],
            data["password"]
        )

        user_data = user.public_data()

        return make_response(jsonify(user_data), 201)
    except:
        return make_response({"Error": "That email is already registered"}, 404)

@api.route('/login', methods=["POST"])
def login_user():
    data = request.get_json(force=True)

    try:
        user = current_app.db.users.find_user(data["email"])

        if not user.verify_password(data["password"]):
            return make_response({"Error": "Invalid email or password"}, 404)
        
        return make_response({"token": "sadasd2a2da"}, 200)
    except:
        return make_response({"Error": "Invalid email or password"}, 404)
