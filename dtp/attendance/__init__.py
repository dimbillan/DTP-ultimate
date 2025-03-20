from flask import Blueprint

attendance = Blueprint('attendance', __name__, url_prefix='/admin')

from . import routes