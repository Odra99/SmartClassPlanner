from app.extensions import db
from app.model.course import *

def getCourseByCode(code):
    return db.session.query(Course).filter_by(code=code).first()

def getAllCourses():
    courses= db.session.query(Course).options(db.joinedload(Course.course_schedule)).all()
    return courses_schema.dump(courses)

def getAllAssignment():
    assignments =  db.session.query(CourseAssignments).all()
    return courses_assignments_schema.dump(assignments)


def getCourseOPByCode(code,scheduleId,area_id):
    return db.session.query(CourseOP).filter_by(code=code,schedule_id=scheduleId,area_id=area_id).first()

def getCourseOPByid(id):
    courseTeacher =  db.session.query(CourseTeacher).filter_by(id=id).first()
    if courseTeacher is not None:
        return db.session.query(Course).filter_by(id=courseTeacher.course_id).first()
    return None