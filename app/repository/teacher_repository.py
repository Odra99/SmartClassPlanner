from app.extensions import db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.model.teacher import *

def getAllTeachers():
    teachers = db.session.query(Teacher).options(db.joinedload(Teacher.teacher_schedule)).all()
    for row in teachers:
        print(row.name)