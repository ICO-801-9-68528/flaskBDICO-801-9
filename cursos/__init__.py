from flask import Blueprint

cursos_bp = Blueprint('cursos', __name__)

from . import routes
