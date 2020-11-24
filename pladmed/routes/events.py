from pladmed import socketio
from flask_socketio import emit

@socketio.on('connect')
def on_connect():
    emit('connected')

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected")

@socketio.on('test_event')
def handle_test_event(msg):
    emit('response', msg)
