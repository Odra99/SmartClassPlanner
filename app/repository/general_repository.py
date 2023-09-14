from app.extensions import db
from app.model.general import *


def getAllArea():
    all_areas =  db.session.query(Area).all()
    return areas_schema.dump(all_areas)

def getAllRestrictions():
    return db.session.query(Restrictions).all()


def getAllPriorityCriteria():
    return db.session.query(PriorityCriteria).all()

def getAreaId(id):
    return db.session.query(Area).filter_by(id=id).first()