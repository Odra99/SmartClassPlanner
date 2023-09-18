from app.extensions import db,ma
from app.model.general import AreaSchema, AreaOPSchema
from app.model.course import CourseTeacherOPSchema
class TeacherSchedule(db.Model):
    __tablename__="teacher_schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'),nullable=True)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id')) 


    teacher = db.relationship('Teacher', back_populates='teacher_schedule')
    area = db.relationship('Area')

class TeacherScheduleSchema(ma.Schema):
    class Meta:
        model=TeacherSchedule
        fields = ("id", "start_time","end_time","area")

    area=ma.Nested(AreaSchema) 


teacher_schedule_schema = TeacherScheduleSchema()
teacher_schedules_schema = TeacherScheduleSchema(many=True)

class Teacher(db.Model):
    __tablename__="teacher"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    teacher_schedule = db.relationship('TeacherSchedule', back_populates='teacher')
    courses = db.relationship('CourseTeacher', back_populates='teacher')

class TeacherSchema(ma.Schema):
    class Meta:
        model=Teacher
        fields = ("id", "name","teacher_schedule")
    teacher_schedule=ma.List(ma.Nested(TeacherScheduleSchema))    

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)


class TeacherScheduleOP(db.Model):
    __tablename__="teacher_schedule_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher_oc.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area_oc.id')) 


    teacher = db.relationship('TeacherOP', back_populates='teacher_schedule')


class TeacherScheduleOPSchema(ma.Schema):
    class Meta:
        model=TeacherScheduleOP
        fields = ("id", "start_time","end_time","area")

    area=ma.Nested(AreaOPSchema) 


teacher_schedule_op_schema = TeacherScheduleOPSchema()
teacher_schedules_op_schema = TeacherScheduleOPSchema(many=True)

class TeacherOP(db.Model):
    __tablename__="teacher_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))

    teacher_schedule = db.relationship('TeacherScheduleOP', back_populates='teacher')
    courses = db.relationship('CourseTeacherOP', back_populates='teachers')
    schedule = db.relationship('Schedule', back_populates='teachers')
    assignment = db.relationship('Assignment', back_populates='teacher')


class TeacherOPSchema(ma.Schema):
    class Meta:
        model=TeacherOP
        fields = ("id", "name","teacher_schedule","courses")
    teacher_schedule=ma.List(ma.Nested(TeacherScheduleOPSchema))
    courses=ma.List(ma.Nested(CourseTeacherOPSchema))    

teacher_op_schema = TeacherOPSchema()
teachers_op_schema = TeacherOPSchema(many=True)
