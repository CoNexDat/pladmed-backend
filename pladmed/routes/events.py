from pladmed import socketio
from flask_socketio import emit
from flask import current_app, request

@socketio.on('connect')
def on_connect():
    emit('connected', "You re connected")
    current_app.probes.append(request.namespace)

@socketio.on('disconnect')
def on_disconnect():
    current_app.probes.remove(request.namespace)    
