from pladmed import socketio
from flask_socketio import emit
from flask import current_app, request
from pladmed.models.probe import Probe
from flask_socketio import ConnectionRefusedError
from pladmed.utils.scamper import warts2text

def find_probe_by_session(session):
    for probe, conn in list(current_app.probes.items()):
        if conn == session:
            return probe
    
    return None

@socketio.on('connect')
def on_connect():
    token = request.args.get('token')

    try:
        probe_data = current_app.token.identity(token)

        probe = current_app.db.probes.find_probe(probe_data["identifier"])

        if probe is None:
            raise ConnectionRefusedError('Invalid token')

        current_app.probes[probe] = request.sid
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

    #TODO Validate if that operation_id is valid for that probe!

    results = warts2text(data["content"])

    current_app.db.operations.add_results(operation, probe, results, unique_code)

    return data["operation_id"]
