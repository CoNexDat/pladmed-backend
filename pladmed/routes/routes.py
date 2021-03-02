from flask import current_app, make_response, jsonify, request, Response
from pladmed.routes import api
from flask_socketio import emit
from pladmed.models.user import User
from pladmed.models.probe import Probe
from pladmed.utils.decorators import user_protected
from pladmed.utils.response import (
    error_response, HTTP_CREATED, HTTP_OK, HTTP_NOT_FOUND, HTTP_BAD_REQUEST,
    HTTP_NO_CONTENT
)
from pladmed.utils.credits_operations import (
    calculate_credits_traceroute
)

def get_available_probes(probes):
    avail_probes = []

    for probe in probes:
        if probe in current_app.probes:
            avail_probes.append(probe)
    
    return avail_probes

def create_operation(name, data, credits_): 
    try:
        user = request.user

        probes = current_app.db.probes.find_selected_probes(data["probes"])

        available_probes = get_available_probes(probes)

        if len(available_probes) == 0:
            return error_response(HTTP_NOT_FOUND, "No available probes")

        operation = current_app.db.operations.create_operation(
            name,
            data["params"],
            available_probes,
            user,
            credits_
        )

        operation_data = operation.public_data()

        do_operation(name, available_probes, operation_data)

        return make_response(operation_data, HTTP_CREATED)
    except:
        return error_response(HTTP_NOT_FOUND, "Invalid data provided")

@api.route('/traceroute', methods=["POST"])
@user_protected
def traceroute():
    #TODO Validate params
    data = request.get_json(force=True)

    total_ips = len(data["params"]["ips"])

    credits_ = calculate_credits_traceroute(total_ips)

    return create_operation("traceroute", data, credits_)

@api.route('/ping', methods=["POST"])
@user_protected
def ping():
    #TODO Validate params
    data = request.get_json(force=True)

    return create_operation("ping", data, 0)

@api.route('/dns', methods=["POST"])
@user_protected
def dns():
    #TODO Validate params
    data = request.get_json(force=True)

    return create_operation("dns", data, 0)

def do_operation(operation, probes, data):
    data_to_send = data.copy()
    del data_to_send["probes"]

    for probe in data["probes"]:
        if probe in current_app.probes:
            emit(operation, data_to_send, room=current_app.probes[probe], namespace='')

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

        return make_response(jsonify(user_data), HTTP_CREATED)
    except:
        return error_response(HTTP_BAD_REQUEST, "That email is already registered")

@api.route('/login', methods=["POST"])
def login_user():
    data = request.get_json(force=True)

    try:
        user = current_app.db.users.find_user(data["email"])

        if not user.verify_password(data["password"]):
            return error_response(HTTP_NOT_FOUND, "Invalid email or password")
        
        user_data = user.public_data()

        access_token = current_app.token.create_token(user_data)

        return make_response({"access_token": access_token}, HTTP_OK)
    except:
        return error_response(HTTP_NOT_FOUND, "Invalid email or password")

@api.route('/users/me', methods=["GET"])
@user_protected
def users_me():
    user = request.user

    user_data = user.public_data()

    return make_response(user_data, HTTP_OK)

@api.route('/probes', methods=["POST"])
@user_protected
def register_probe():
    user = request.user

    probe = current_app.db.probes.create_probe(user)

    token = current_app.token.create_token(probe.public_data())

    return make_response({"token": token}, HTTP_CREATED)

@api.route('/probes', methods=["GET"])
def all_probes():
    probes = current_app.db.probes.find_all_probes()

    return make_response(jsonify(probes), HTTP_OK)

@api.route('/delete_all', methods=["DELETE"])
def delete_all():
    if current_app.config["ENV"] == "production":
        return Response(status=HTTP_NOT_FOUND)

    current_app.db.reset_db()

    return Response(status=HTTP_NO_CONTENT)

@api.route('/operation', methods=["GET"])
def operation():
    op_id = request.args.get('id')

    try:
        operation = current_app.db.operations.find_operation(op_id)

        operation_data = operation.public_data()

        return make_response(operation_data, HTTP_OK)
    except:
        return error_response(HTTP_NOT_FOUND, "Operation doesn't exists")
