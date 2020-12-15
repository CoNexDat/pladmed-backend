from functools import wraps
from flask import current_app, make_response, request

def user_protected(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("access_token")

        if access_token is None:
            return make_response({"Error": "No authorization to access this content"}, 403)

        try:
            data = current_app.token.identity(access_token)

            user = current_app.db.users.find_user(data["email"])

            if not user:
                return make_response({"Error": "No authorization to access this content"}, 403)

            request.user = user

            return func(*args, **kwargs)
        except:
            return make_response({"Error": "No authorization to access this content"}, 403)

    return decorated_function
