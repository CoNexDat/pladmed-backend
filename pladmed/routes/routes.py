from flask import current_app, make_response, jsonify, request, Response
from pladmed.routes import api
from flask_socketio import emit
from pladmed.models.user import User
from pladmed.models.probe import Probe
from pladmed.utils.decorators import user_protected, superuser
from pladmed.utils.response import (
    error_response, HTTP_CREATED, HTTP_OK, HTTP_NOT_FOUND, HTTP_BAD_REQUEST,
    HTTP_NO_CONTENT
)
from pladmed.utils.credits_operations import (
    calculate_credits_traceroute,
    calculate_credits_ping,
    calculate_credits_dns
)
from pladmed import socketio
from pladmed.validators.route_validator import (
    validate_traceroute, validate_ping, validate_dns, validate_user_data, validate_user_data_present,
    validate_credits, validate_location
)


def got_enough_credits(conn, credits_):
    return conn.in_use_credits + credits_ <= conn.total_credits


def get_available_probes(probes, credits_):
    avail_probes = []

    for probe in probes:
        if (
            probe in current_app.probes and
            got_enough_credits(current_app.probes[probe], credits_)
        ):
            avail_probes.append(probe)

    return avail_probes


def create_operation(name, data, credits_per_probe, result_format):
    try:
        user = request.user

        probes = current_app.db.probes.find_selected_probes(data["probes"])

        available_probes = get_available_probes(probes, credits_per_probe)

        if len(available_probes) == 0:
            return error_response(HTTP_NOT_FOUND, "No available probes")

        total_credits = credits_per_probe * len(available_probes)

        operation = current_app.db.operations.create_operation(
            name,
            data["params"],
            available_probes,
            user,
            total_credits,
            result_format
        )

        operation_data = operation.public_data()

        if user.credits - total_credits < 0:
            return error_response(HTTP_BAD_REQUEST, "Not enough credits")

        current_app.db.users.change_credits(user, user.credits - total_credits)

        do_operation(name, available_probes, operation_data, credits_per_probe)

        return make_response(operation_data, HTTP_CREATED)
    except:
        return error_response(HTTP_NOT_FOUND, "Invalid data provided")


@api.route('/traceroute', methods=["POST"])
@user_protected
def traceroute():
    data = request.get_json(force=True)

    if not validate_traceroute(data):
        return error_response(HTTP_BAD_REQUEST, "Invalid data provided")

    total_destinations = count_destinations(data["params"])

    credits_ = calculate_credits_traceroute(total_destinations)

    return create_operation("traceroute", data, credits_, data["result_format"])


@api.route('/ping', methods=["POST"])
@user_protected
def ping():
    data = request.get_json(force=True)

    if not validate_ping(data):
        return error_response(HTTP_BAD_REQUEST, "Invalid data provided")

    total_destinations = count_destinations(data["params"])

    credits_ = calculate_credits_ping(total_destinations)

    return create_operation("ping", data, credits_, "json")


@api.route('/dns', methods=["POST"])
@user_protected
def dns():
    data = request.get_json(force=True)

    if not validate_dns(data):
        return error_response(HTTP_BAD_REQUEST, "Invalid data provided")

    total_destinations = count_destinations(data["params"])

    credits_per_probe = calculate_credits_dns(total_destinations)

    return create_operation("dns", data, credits_per_probe, "text")


def count_destinations(params):
    total_destinations = 0
    if "fqdns" in params:
        total_destinations += len(params["fqdns"])
    if "ips" in params:
        total_destinations += len(params["ips"])
    return total_destinations


def do_operation(operation, probes, data, credits_per_probe):
    data_to_send = data.copy()

    del data_to_send["probes"]

    data_to_send["credits"] = credits_per_probe

    for probe in data["probes"]:
        if probe in current_app.probes:
            socketio.emit(
                operation,
                data_to_send,
                room=current_app.probes[probe].sid,
                namespace=''
            )


@api.route('/register', methods=["POST"])
def create_user():
    data = request.get_json(force=True)

    validation_error = validate_user_data(data)
    if validation_error != "":
        return error_response(HTTP_BAD_REQUEST, validation_error)

    try:
        user = current_app.db.users.create_user(
            email=data["email"],
            password=data["password"],
            is_superuser=False,
            credits_=0
        )

        user_data = user.public_data()

        return make_response(jsonify(user_data), HTTP_CREATED)
    except:
        return error_response(HTTP_BAD_REQUEST, "That email is already registered")


@api.route('/login', methods=["POST"])
def login_user():
    data = request.get_json(force=True)

    validation_error = validate_user_data_present(data)
    if validation_error != "":
        return error_response(HTTP_BAD_REQUEST, validation_error)

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
    location_json = request.get_json(force=True)

    validation_error = validate_location(location_json)
    if validation_error != "":
        return error_response(HTTP_BAD_REQUEST, validation_error)

    location = location_json["location"]

    probe = current_app.db.probes.create_probe(user, location)

    token = current_app.token.create_token(probe.public_data())

    return make_response({"token": token}, HTTP_CREATED)


@api.route('/probes', methods=["GET"])
def all_probes():
    probes = current_app.db.probes.find_all_probes()

    probes_data = []

    for probe in probes:
        data = probe.public_data()
        data["connected"] = False

        if probe in current_app.probes:
            conn = current_app.probes[probe]

            data["connected"] = True
            data["availability"] = 1.0 - conn.in_use_credits / conn.total_credits
        
        probes_data.append(data)

    return make_response(jsonify(probes_data), HTTP_OK)


@api.route('/probes/me', methods=["GET"])
@user_protected
def probes_by_user():
    user = request.user
    probes = current_app.db.probes.find_by_user(user._id)

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
        return error_response(HTTP_NOT_FOUND, "Operation doesn't exist")


@api.route('/credits', methods=["POST"])
@superuser
def give_credits():
    data = request.get_json(force=True)

    if not validate_credits(data):
        return error_response(HTTP_BAD_REQUEST, "Invalid data provided")

    try:
        user = current_app.db.users.find_user_by_id(data["id"])

        current_app.db.users.change_credits(
            user, user.credits + data["credits"])

        return make_response(user.public_data(), HTTP_OK)
    except:
        return error_response(HTTP_NOT_FOUND, "User doesn't exist")
