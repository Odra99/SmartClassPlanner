from app.extensions import db
from app.model.schedule import *
from app.enums import StatusEnum

def getInProgressSchedule():
    return db.session.query(Schedule).filter_by(parent_id=None,status=StatusEnum.IN_PROGRESS.value)