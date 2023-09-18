from app.extensions import db,ma
from app.model.course import CourseOPSchema
from app.model.teacher import TeacherOPSchema
from app.model.classE import ClassOPSchema
from app.model.assignment import AssignmentSchema


class ScheduleRestrictions(db.Model):
    __tablename__="schedule_restriction"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    type = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    name = db.Column(db.String(150), nullable=False)
    value = db.Column(db.String(150), nullable=False)

    schedule = db.relationship('Schedule', back_populates='restrictions')

class ScheduleRestrictionsSchema(ma.Schema):
    class Meta:
        model=ScheduleRestrictions
        fields = ("id", "name","value")
class Schedule(db.Model):
    __tablename__="schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    parent_id = db.Column(db.BIGINT, nullable=True)
    date = db.Column(db.TIMESTAMP,nullable=False)
    priority_criterias = db.relationship('ScheduleConfigurationPriorityCriteria', back_populates='schedule')
    classes_configurations = db.relationship('ClassOP', back_populates='schedule')
    courses = db.relationship('CourseOP', back_populates='schedule')
    restrictions = db.relationship('ScheduleRestrictions', back_populates='schedule')
    area_configurations = db.relationship('ScheduleAreaConfiguration', back_populates='schedule')
    teachers = db.relationship('TeacherOP', back_populates='schedule')
    assignments = db.relationship('Assignment', back_populates='schedule')
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    version = db.Column(db.Integer, nullable=False)

    matrixAssingments = []

class ScheduleSchema(ma.Schema):
    class Meta:
        model=Schedule
        fields = ("id", "name","courses","teachers","classes_configurations","assignments","status","version","date","parent_id","restrictions","matrixAssingments")
    courses=ma.List(ma.Nested(CourseOPSchema))
    teachers=ma.List(ma.Nested(TeacherOPSchema))
    classes_configurations = ma.List(ma.Nested(ClassOPSchema))
    assignments = ma.List(ma.Nested(AssignmentSchema))
    restrictions = ma.List(ma.Nested(ScheduleRestrictionsSchema))

schedule_schema = ScheduleSchema() 
schedules_schema = ScheduleSchema(many=True)


class ScheduleConfigurationPriorityCriteria(db.Model):
    __tablename__="schedule_configuration_priority_criteria"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    type = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    subtype = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    description = db.Column(db.String(100), nullable=False)
    asc = db.Column(db.Boolean,nullable=False,default=True)
    order = db.Column(db.Integer, nullable=False)


    schedule = db.relationship('Schedule', back_populates='priority_criterias')

class ScheduleAreaConfiguration(db.Model):
    __tablename__="schedule_area_configuration"
    id = db.Column(db.BIGINT, primary_key=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area_oc.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    priority = db.Column(db.Integer, nullable=False)

    schedule = db.relationship('Schedule', back_populates='area_configurations')

