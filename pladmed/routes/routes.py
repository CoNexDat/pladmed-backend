from flask import current_app, make_response, jsonify, request
from pladmed.routes import api
from flask_socketio import emit

@api.route('/operation', methods=["POST"])
def create_operation():
    data = request.get_json(force=True) 

    for conn, probe in current_app.probes.items():
        if probe.identifier in data["probes"]:
            emit("operation", room=conn, namespace='')

    return make_response(data, 201)
