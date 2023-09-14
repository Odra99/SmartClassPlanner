from app.extensions import db
from app.model.classE import Class, classes_schema


def getAll():
    classes = db.session.query(Class).options(db.joinedload(Class.class_schedule)).all()
    return classes_schema.dump(classes)