from app.extensions import db
from app.model.schedule import *
from app.enums import StatusEnum
from app.main.schedule.scheduleFunctions import matrixGenerator
from sqlalchemy import desc,asc


def getInProgressSchedule():
    schedule = db.session.query(Schedule).filter_by(status=StatusEnum.IN_PROGRESS.value).order_by(asc(Schedule.version)).first()
    if(schedule is not None):
        schedule.matrixAssingments = matrixGenerator(schedule)
    return schedule

def getChildSchedules(id):
    schedules = db.session.query(Schedule).filter_by(
        parent_id=id).order_by(asc(Schedule.version)).all()
    return schedules

def getScheduleById(id):
    schedules = db.session.query(Schedule).filter_by(id=id).order_by(asc(Schedule.version)).first()
    return schedules


def getInProgressScheduleF():
    schedule = db.session.query(Schedule).filter_by(parent_id=None, status=StatusEnum.IN_PROGRESS.value).order_by(desc(Schedule.version)).first()
    if(schedule is not None):
        schedule.matrixAssingments = matrixGenerator(schedule)
    return schedule



