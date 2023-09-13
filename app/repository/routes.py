from app.repository import bp
from flask import (request, jsonify)
from app.repository import *


pathArea = '/area'


@bp.route(pathArea, methods=['GET'])
def classLoad():
    if request.method == 'GET':
        areas = general_repository.getAllArea()
        return jsonify(areas), 200
    return jsonify(), 400
