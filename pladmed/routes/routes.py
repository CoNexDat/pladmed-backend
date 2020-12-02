from flask import current_app, make_response, jsonify, request
from pladmed.routes import api
from flask_socketio import emit


@api.route('/traceroute', methods=["POST"])
def traceroute():
    data = request.get_json(force=True)

    # TODO Validate data and params

    # TODO Save operation in db

    do_operation("traceroute", data)

    return make_response(data, 201)

@api.route('/ping', methods=["POST"])
def ping():
    data = request.get_json(force=True)
    # TODO Validate data and params

    # TODO Save operation in db
    do_operation("ping", data)

    return make_response(data, 201)

@api.route('/dns', methods=["POST"])
def dns():
    data = request.get_json(force=True)
    # TODO Validate data and params

    # TODO Save operation in db
    do_operation("dns", data)

    return make_response(data, 201)

def do_operation(operation, data):
    for conn, probe in list(current_app.probes.items()):
        if probe.identifier in data["probes"]:
            emit(operation, data, room=conn, namespace='')

