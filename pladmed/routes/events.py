from pladmed import socketio
from flask_socketio import emit
from flask import current_app, request
from pladmed.models.probe import Probe
from flask_socketio import ConnectionRefusedError

@socketio.on('connect')
def on_connect():
    token = request.args.get('token')

    if not token:
        raise ConnectionRefusedError('Invalid token')

    probe = current_app.token.identity(token)

    if not probe:
        # Refuse connection if no probe exists with that token
        raise ConnectionRefusedError('Invalid token')

    current_app.probes[request.sid] = Probe("identifier")


@socketio.on('disconnect')
def on_disconnect():
    del current_app.probes[request.sid]
