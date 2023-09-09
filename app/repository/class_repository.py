from app.extensions import db
from app.model.classE import *


def getAll():
    return db.session.query(Class).options(db.joinedload(Class.class_schedule)).all()
