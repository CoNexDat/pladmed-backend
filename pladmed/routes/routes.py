from flask import current_app, make_response, jsonify, request
from pladmed.routes import api
from flask_socketio import emit
from pladmed.models.user import User
from pladmed.models.probe import Probe
from pladmed.utils.decorators import user_protected

def create_operation(name): 
    try:
        user = request.user
        data = request.get_json(force=True)

        probes = current_app.db.probes.find_selected_probes(data["probes"])

        operation = current_app.db.operations.create_operation(
            name,
            data["params"],
            probes,
            user
        )

        operation_data = operation.public_data()

        do_operation(name, operation_data)

        return make_response(operation_data, 201)
    except:
        return make_response({"Error": "Invalid data provided"}, 404)    

@api.route('/traceroute', methods=["POST"])
@user_protected
def traceroute():
    #TODO Validate params

    return create_operation("traceroute")

@api.route('/ping', methods=["POST"])
@user_protected
def ping():
    #TODO Validate params

    return create_operation("ping")

@api.route('/dns', methods=["POST"])
@user_protected
def dns():
    #TODO Validate params

    return create_operation("dns")

def do_operation(operation, data):
    # TODO: Change this, we don't want to travel all the probes...
    for conn, probe in list(current_app.probes.items()):
        for data_probes in data["probes"]:
            if probe.identifier == data_probes["identifier"]:
                emit(operation, data, room=conn, namespace='')

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
