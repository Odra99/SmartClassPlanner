from app.extensions import db
from app.model.general import *


def getAllArea():
    all_areas =  db.session.query(Area).all()
    return areas_schema.dump(all_areas)

def getAllRestrictions():
    all_restrictions =  db.session.query(Restrictions).all()
    return restrictions_schema.dump(all_restrictions)


def getAllPriorityCriteria():
    all_priorities= db.session.query(PriorityCriteria).all()
    return priority_criterias_schema.dump(all_priorities)

def getAreaId(id):
    return db.session.query(Area).filter_by(id=id).first()