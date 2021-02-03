from flask import current_app, make_response, jsonify, request
from pladmed.routes import api
from flask_socketio import emit
from pladmed.models.user import User
from pladmed.models.probe import Probe
from pladmed.utils.decorators import user_protected

@api.route('/traceroute', methods=["POST"])
@user_protected
def traceroute():
    try:
        user = request.user
        data = request.get_json(force=True)

        # TODO Validate data and params

        probes = current_app.db.probes.find_selected_probes(data["probes"])

        operation = current_app.db.operations.create_operation(
            "traceroute",
            data["params"],
            probes,
            user
        )

        operation_data = operation.public_data()

        do_operation("traceroute", data)

        return make_response(operation_data, 201)
    except:
        return make_response({"Error": "Invalid data provided"}, 404)

@api.route('/ping', methods=["POST"])
@user_protected
def ping():
    try:
        user = request.user
        data = request.get_json(force=True)
        # TODO Validate data and params

        probes = current_app.db.probes.find_selected_probes(data["probes"])

        operation = current_app.db.operations.create_operation(
            "ping",
            data["params"],
            probes,
            user
        )

        operation_data = operation.public_data()

        do_operation("ping", data)

        return make_response(operation_data, 201)
    except:
        return make_response({"Error": "Invalid data provided"}, 404)

@api.route('/dns', methods=["POST"])
@user_protected
def dns():
    data = request.get_json(force=True)
    # TODO Validate data and params

    # TODO Save operation in db
    do_operation("dns", data)

    return make_response(data, 201)

def do_operation(operation, data):
    # TODO: Change this, we don't want to travel all the probes...
    for conn, probe in list(current_app.probes.items()):
        if probe.identifier in data["probes"]:
            emit(operation, data, room=conn, namespace='')
    '''        for data_probes in data["probes"]:
            if probe.identifier == data_probes["identifier"]:
                emit(operation, data, room=conn, namespace='')'''
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
        
        user_data = user.public_data()

        access_token = current_app.token.create_token(user_data)

        return make_response({"access_token": access_token}, 200)
    except:
        return make_response({"Error": "Invalid email or password"}, 404)

@api.route('/users/me', methods=["GET"])
@user_protected
def users_me():
    user = request.user

    user_data = user.public_data()

    return make_response(user_data, 200)

@api.route('/probes', methods=["POST"])
@user_protected
def register_probe():
    user = request.user

    probe = current_app.db.probes.create_probe(user)

    token = current_app.token.create_token(probe.public_data())

    return make_response({"token": token}, 201)

@api.route('/probes', methods=["GET"])
def all_probes():
    probes = current_app.db.probes.find_all_probes()

    return make_response(jsonify(probes), 200)
