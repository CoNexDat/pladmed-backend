from flask import current_app, make_response, jsonify, request, Response

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_NO_AUTH = 403

def error_response(status_code, error):
    return make_response({"Error": error}, status_code)
