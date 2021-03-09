from functools import wraps
from flask import current_app, request
from pladmed.utils.response import error_response, HTTP_NO_AUTH

def parse_user(func, superuser, *args, **kwargs):
    access_token = request.headers.get("access_token")

    if access_token is None:
        return error_response(
            HTTP_NO_AUTH, "No authorization to access this content"
        )

    try:
        data = current_app.token.identity(access_token)

        user = current_app.db.users.find_user(data["email"])

        if not user or (superuser and not user.is_superuser):
            return error_response(
                HTTP_NO_AUTH, "No authorization to access this content"
            )

        request.user = user

        return func(*args, **kwargs)
    except:
        return error_response(
            HTTP_NO_AUTH, "No authorization to access this content"
        )    

def user_protected(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return parse_user(func, False, *args, **kwargs)

    return decorated_function

def superuser(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return parse_user(func, True, *args, **kwargs)

    return decorated_function
