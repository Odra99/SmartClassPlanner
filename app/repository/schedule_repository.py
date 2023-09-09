from app.extensions import db
from app.model.schedule import *
from app.enums import StatusEnum

def getInProgressSchedule():
    return db.session.query(Schedule).filter_by(status=StatusEnum.IN_PROGRESS.value).first()