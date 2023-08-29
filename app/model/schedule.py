from app.extensions import db

class Schedule(db.Model):
    __tablename__="schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    parent_id = db.Column(db.BIGINT, nullable=False)
    date = db.Column(db.TIMESTAMP,nullable=False)
    priority_criteria = db.relationship('ScheduleConfigurationPriorityCriteria', backref='priority_criteria')
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    version = db.Column(db.Integer, db.ForeignKey('type.id'))


class ScheduleConfigurationPriorityCriteria(db.Model):
    __tablename__="schedule_configuration_priority_criteria"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    priority_criteria_id = db.Column(db.BIGINT,  db.ForeignKey('priority_criteria.id'))

class ScheduleAreaConfiguration(db.Model):
    __tablename__="schedule_area_configuration"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))

class ScheduleClassConfiguration(db.Model):
    __tablename__="schedule_class_configuration"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    class_id = db.Column(db.BIGINT,  db.ForeignKey('class.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id'))
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))

class Restrictions(db.Model):
    __tablename__="restriction"
    id = db.Column(db.BIGINT, primary_key=True)
    type = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    name = db.Column(db.String(150), nullable=False)
    value = db.Column(db.String(150), nullable=False)

