from pladmed import socketio
from flask_socketio import emit
from flask import current_app, request
from pladmed.models.probe import Probe
from flask_socketio import ConnectionRefusedError
from jwt.exceptions import DecodeError

@socketio.on('connect')
def on_connect():
    token = request.args.get('token')

    if not token:
        raise ConnectionRefusedError('Invalid token')

    try:
        probe_data = current_app.token.identity(token)

        probe = current_app.db.probes.find_probe(probe_data["identifier"])

        if probe is None:
            raise ConnectionRefusedError('Invalid token')

        current_app.probes[request.sid] = Probe("identifier")
    except DecodeError:
        # Raising something in except is bad, but we can't do it better for now
        raise ConnectionRefusedError('Invalid token')

@socketio.on('disconnect')
def on_disconnect():
    del current_app.probes[request.sid]
