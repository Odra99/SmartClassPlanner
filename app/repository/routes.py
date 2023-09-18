from app.repository import bp
from app.extensions import db
from flask import (request, jsonify)
from app.repository import *
from app.repository.schedule_repository import schedule_schema
from app.main.schedule.schedule import scheduleGeneration
from app.model.schedule import Schedule
from functools import wraps


pathArea = '/area'
pathTeacher = '/teacher'
pathClassroom = '/classroom'
pathCourse = '/course'
pathSchedule = '/schedule'
pathRestriction = '/restriction'
pathPriority = '/priority'

def convert_input_to(class_):
    def wrap(f):
        def decorator(*args):
            obj = class_(**request.get_json())
            return f(obj)
        return decorator
    return wrap



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

@bp.route(pathSchedule, methods=['GET'])
def getSchedule():
    if request.method == 'GET':
        schedule = schedule_repository.getInProgressSchedule()
        return jsonify(schedule_schema.dump(schedule)), 200
    return jsonify(), 400

@bp.route(pathRestriction, methods=['GET'])
def getRestrictions():
    if request.method == 'GET':
        restriction = general_repository.getAllRestrictions()
        return jsonify(restriction), 200
    return jsonify(), 400

@bp.route(pathPriority, methods=['GET'])
def getPriority():
    if request.method == 'GET':
        priority = general_repository.getAllPriorityCriteria()
        return jsonify((priority)), 200
    return jsonify(), 400

@bp.route(pathSchedule+"/generate",methods=['POST'])
def generateSchedule():
    schedule = request.get_json()
    sched = schedule_schema.load(schedule)
    scheduleGeneration(sched)

    return jsonify(), 200

