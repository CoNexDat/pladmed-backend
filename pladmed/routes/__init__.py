from flask import Blueprint

api = Blueprint('api', __name__)
superuser = Blueprint('superuser', __name__)

from . import routes, events, commands
