from app.extensions import db
from app.model.general import *


def getAllArea():
    return db.session.query(Area).all()

def getAllRestrictions():
    return db.session.query(Restrictions).all()


def getAllPriorityCriteria():
    return db.session.query(PriorityCriteria).all()