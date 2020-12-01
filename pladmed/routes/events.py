from pladmed import socketio
from flask_socketio import emit
from flask import current_app, request
from pladmed.models.probe import Probe
from flask import current_app, request, jsonify


@socketio.on('connect')
def on_connect():
    current_app.probes[request.sid] = Probe("identifier")


@socketio.on('disconnect')
def on_disconnect():
    del current_app.probes[request.sid]
