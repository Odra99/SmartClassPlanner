from app.extensions import db
from app.model.teacher import *

def getAllTeachers():
    teachers = db.session.query(Teacher).options(db.joinedload(Teacher.teacher_schedule)).options(db.joinedload(Teacher.courses)).all()
    return teachers_schema.dump(teachers)
