from app.extensions import db

class Schedule(db.Model):
    __tablename__="schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    parent_id = db.Column(db.BIGINT, nullable=True)
    date = db.Column(db.TIMESTAMP,nullable=False)
    priority_criterias = db.relationship('ScheduleConfigurationPriorityCriteria', back_populates='schedule')
    classes_configurations = db.relationship('ScheduleClassConfiguration', back_populates='schedule')
    courses = db.relationship('CourseOP', back_populates='schedule')
    restrictions = db.relationship('ScheduleRestrictions', back_populates='schedule')
    area_configurations = db.relationship('ScheduleAreaConfiguration', back_populates='schedule')
    teachers = db.relationship('TeacherOP', back_populates='schedule')
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    version = db.Column(db.Integer, nullable=False)


class ScheduleConfigurationPriorityCriteria(db.Model):
    __tablename__="schedule_configuration_priority_criteria"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    priority_criteria_id = db.Column(db.BIGINT,  db.ForeignKey('priority_criteria.id'))

    schedule = db.relationship('Schedule', back_populates='priority_criterias')

class ScheduleAreaConfiguration(db.Model):
    __tablename__="schedule_area_configuration"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    priority = db.Column(db.Integer, nullable=False)

    schedule = db.relationship('Schedule', back_populates='area_configurations')

class ScheduleClassConfiguration(db.Model):
    __tablename__="schedule_class_configuration"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    class_id = db.Column(db.BIGINT,  db.ForeignKey('class_oc.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id'))
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))

    schedule = db.relationship('Schedule', back_populates='classes_configurations')

class ScheduleRestrictions(db.Model):
    __tablename__="schedule_restriction"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    type = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    name = db.Column(db.String(150), nullable=False)
    value = db.Column(db.String(150), nullable=False)

    schedule = db.relationship('Schedule', back_populates='restrictions')

