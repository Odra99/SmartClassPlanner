from app.extensions import db
from app.model.teacher import *

def getAllTeachers():
    teachers = db.session.query(Teacher).options(db.joinedload(Teacher.teacher_schedule)).all()
    for row in teachers:
        print(row.name)
