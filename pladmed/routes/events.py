from pladmed import socketio
from flask_socketio import emit
from flask import current_app, request
from pladmed.models.probe import Probe
from flask_socketio import ConnectionRefusedError
from pladmed.utils.scamper import gzip2text, warts2json, warts2dump
from pladmed.models.connection import Connection
from pladmed.utils.credits_operations import CREDITS_PER_RESULT

def find_probe_by_session(session):
    for probe, conn in list(current_app.probes.items()):
        if conn.sid == session:
            return probe

    return None


@socketio.on('connect')
def on_connect():
    token = request.args.get('token')
    total_credits = int(request.headers.get("Total-Credits"))
    in_use_credits = int(request.headers.get("In-Use-Credits"))

    try:
        probe_data = current_app.token.identity(token)

        probe = current_app.db.probes.find_probe(probe_data["identifier"])

        if probe is None:
            raise ConnectionRefusedError('Invalid token')

        conn = Connection(request.sid, total_credits, in_use_credits)

        current_app.probes[probe] = conn
    except:
        # Raising something in except is bad, but we can't do it better for now
        raise ConnectionRefusedError('Invalid token')


@socketio.on('disconnect')
def on_disconnect():
    probe = find_probe_by_session(request.sid)

    if probe is not None:
        del current_app.probes[probe]


@socketio.on('results')
def on_results(data):
    probe = find_probe_by_session(request.sid)

    # Probe suddenly got disconnected so i can't find it's model
    if probe is None:
        return None

    unique_code = data["unique_code"]

    operation = current_app.db.operations.find_operation(data["operation_id"])

    if operation.code_exists(unique_code):
        # If that code already exists, filter it and return operation_id
        # so that the client doesn't know that it was dup
        return data["operation_id"]

    # TODO Validate if that operation_id is valid for that probe!

    results = ""

    if data["format"] == "warts":
        results = warts2dump(data["content"])
    elif data["format"] == "gzip":
        results = gzip2text(data["content"])

    current_app.db.operations.add_results(
        operation, probe, results, unique_code
    )

    user = current_app.db.users.find_user_by_id(probe.owner_id)

    current_app.db.users.change_credits(user, user.credits + CREDITS_PER_RESULT)

    return data["operation_id"]

@socketio.on('new_operation')
def on_new_operation(data):
    probe = find_probe_by_session(request.sid)

    # Probe suddenly got disconnected so i can't find it's model
    if probe is None:
        return

    credits_ = data["credits"]

    current_app.probes[probe].in_use_credits += credits_

@socketio.on('finish_operation')
def on_finish_operation(data):
    probe = find_probe_by_session(request.sid)

    # Probe suddenly got disconnected so i can't find it's model
    if probe is None:
        return

    credits_ = data["credits"]

    current_app.probes[probe].in_use_credits -= credits_
