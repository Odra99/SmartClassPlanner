from app.extensions import db
from app.model.course import *

def getCourseByCode(code):
    return db.session.query(Course).filter_by(code=code).first()
