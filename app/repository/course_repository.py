from app.extensions import db
from app.model.course import *

def getCourseByCode(code):
    return db.session.query(Course).filter_by(code=code).first()

def getAllCourses():
    return db.session.query(Course).options(db.joinedload(Course.course_schedule)).all()

def getAllAssignment():
    return db.session.query(CourseAssignments).all()


def getCourseOPByCode(code,scheduleId):
    return db.session.query(CourseOP).filter_by(code=code,schedule_id=scheduleId).first()