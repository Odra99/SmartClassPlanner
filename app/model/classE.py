from app.extensions import db, ma
from app.model.general import AreaSchema, AreaOPSchema


class ClassSchedule(db.Model):
    __tablename__ = "class_schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'), nullable=True)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    class_id = db.Column(db.BIGINT, db.ForeignKey('class.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id'))

    classE = db.relationship('Class', back_populates='class_schedule')

    area_name=""


class ClassScheduleSchema(ma.Schema):
    class Meta:
        model = ClassSchedule
        fields = ("id", "start_time", "end_time", "area","area_name")

    area = ma.Nested(AreaSchema)


class Class(db.Model):
    __tablename__ = "class"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    space_capacity = db.Column(db.Integer, nullable=False)

    class_schedule = db.relationship('ClassSchedule', back_populates='classE')


class ClassSchema(ma.Schema):
    class Meta:
        model = Class
        fields = ("id", "name", "space_capacity", "class_schedule")
    class_schedule = ma.List(ma.Nested(ClassScheduleSchema))


class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)



class ClassScheduleOP(db.Model):
    __tablename__ = "class_schedule_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'), nullable=True)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    class_id = db.Column(db.BIGINT, db.ForeignKey('class_oc.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area_oc.id'))

    classE = db.relationship('ClassOP', back_populates='class_schedule')

    area_name=""


class ClassScheduleOPSchema(ma.Schema):
    class Meta:
        model = ClassScheduleOP
        fields = ("id", "start_time", "end_time", "area","area_name")

    area = ma.Nested(AreaOPSchema)

class ClassOP(db.Model):
    __tablename__ = "class_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    space_capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.BIGINT, db.ForeignKey('type.id'))

    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))
    

    class_schedule = db.relationship(
        'ClassScheduleOP', back_populates='classE')
    schedule = db.relationship(
        'Schedule', back_populates='classes_configurations')
    assignment = db.relationship('Assignment', back_populates='classroom')

    
class ClassOPSchema(ma.Schema):
    class Meta:
        model = ClassOP
        fields = ("id", "name", "space_capacity", "class_schedule")
    class_schedule = ma.List(ma.Nested(ClassScheduleOPSchema))


class_op_schema = ClassOPSchema()
classes_op_schema = ClassOPSchema(many=True)


