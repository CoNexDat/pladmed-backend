from functools import wraps
from flask import current_app, request
from pladmed.utils.response import error_response, HTTP_NO_AUTH

def user_protected(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("access_token")

        if access_token is None:
            return error_response(
                HTTP_NO_AUTH, "No authorization to access this content"
            )

        try:
            data = current_app.token.identity(access_token)

            user = current_app.db.users.find_user(data["email"])

            if not user:
                return error_response(
                    HTTP_NO_AUTH, "No authorization to access this content"
                )

            request.user = user

            return func(*args, **kwargs)
        except:
            return error_response(
                HTTP_NO_AUTH, "No authorization to access this content"
            )

    return decorated_function
