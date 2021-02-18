from pladmed import socketio
from flask_socketio import emit
from flask import current_app, request
from pladmed.models.probe import Probe
from flask_socketio import ConnectionRefusedError
from pladmed.utils.scamper import warts2text

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
    for probe, conn in list(current_app.probes.items()):
        if conn == request.sid:
            del current_app.probes[probe]

@socketio.on('results')
def on_results(data):
    # Should validate if that operation_id is from that probe!
    results = warts2text(data["content"])

    return data["operation_id"]
