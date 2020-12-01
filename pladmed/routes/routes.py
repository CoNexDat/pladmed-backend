from flask import current_app, make_response, jsonify, request
from pladmed.routes import api

@api.route('/operation', methods=["POST"])
def create_operation():
    data = request.get_json(force=True) 

    return make_response(data, 201)
