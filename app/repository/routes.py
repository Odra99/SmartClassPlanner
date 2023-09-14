from app.repository import bp
from app.extensions import db
from flask import (request, jsonify)
from app.repository import *


pathArea = '/area'
pathTeacher = '/teacher'
pathClassroom = '/classroom'
pathCourse = '/course'


@bp.route(pathArea, methods=['GET'])
def getAreas():
    if request.method == 'GET':
        areas = general_repository.getAllArea()
        return jsonify(areas), 200
    return jsonify(), 400

@bp.route(pathArea+"/<id>",methods=['PUT'])
def updateArea(id):
    if request.method == 'PUT':
        area = general_repository.getAreaId(id)      
        if area is None:
            return jsonify(), 404
        name = request.json['name']
        color = request.json['color']
        area.color = color
        area.name = name
        db.session.commit()
        return jsonify(), 200
    return jsonify(), 400

@bp.route(pathTeacher, methods=['GET'])
def getTeachers():
    if request.method == 'GET':
        teachers = teacher_repository.getAllTeachers()
        return jsonify(teachers), 200
    return jsonify(), 400


@bp.route(pathClassroom, methods=['GET'])
def getClassrooms():
    if request.method == 'GET':
        classrooms = class_repository.getAll()
        return jsonify(classrooms), 200
    return jsonify(), 400

@bp.route(pathCourse, methods=['GET'])
def getCourses():
    if request.method == 'GET':
        courses = course_repository.getAllCourses()
        return jsonify(courses), 200
    return jsonify(), 400