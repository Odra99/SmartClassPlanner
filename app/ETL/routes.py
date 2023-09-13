from app.ETL import bp
from flask import (request, jsonify)
from app.ETL.classETL import *
from app.ETL.teacherETL import *
from app.ETL.generalETL import *
from app.ETL.courseETL import *

path = "/etl"


@bp.route(path+'/class', methods=['POST'])
def classLoad():
    if request.method == 'POST':
        json = request.json
        classesCSV = json.get('classCSV')
        classesScheduleCSV = json.get('classScheduleCSV')
        etlCLass(classesCSV, classesScheduleCSV)
        return jsonify(), 200
    return jsonify(), 400


@bp.route(path+'/teacher', methods=['POST'])
def teacherLoad():
    if request.method == 'POST':
        json = request.json
        teacherCSV = json.get('teacherCSV')
        teacherScheduleCSV = json.get('teacherScheduleCSV')
        teacherCourseCSV = json.get('teacherCourseCSV')
        etlTeacher(teacherCSV, teacherScheduleCSV,teacherCourseCSV)
        return jsonify(), 200
    return jsonify(), 400

@bp.route(path+'/area', methods=['POST'])
def areaLoad():
    if request.method == 'POST':
        json = request.json
        areaCSV = json.get('areaCSV')
        etlArea(areaCSV)
        return jsonify(), 200
    return jsonify(), 400

@bp.route(path+'/course', methods=['POST'])
def courseLoad():
    if request.method == 'POST':
        json = request.json
        courseCSV = json.get('courseCSV')
        courseScheduleCSV = json.get('courseScheduleCSV')
        etlCourse(courseCSV, courseScheduleCSV)
        return jsonify(), 200
    return jsonify(), 400

@bp.route(path+'/assignment', methods=['POST'])
def courseAssignmentLoad():
    if request.method == 'POST':
        json = request.json
        courseCSV = json.get('courseAssignmentCSV')
        etlCourseAssignment(courseCSV)
        return jsonify(), 200
    return jsonify(), 400
