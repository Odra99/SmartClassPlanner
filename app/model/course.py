from app.extensions import db,ma
from app.model.general import AreaSchema, AreaOPSchema

class CourseSchedule(db.Model):
    __tablename__="course_schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id'),nullable=True) 


    course = db.relationship('Course', back_populates='course_schedule')

class CourseScheduleSchema(ma.Schema):
    class Meta:
        model = CourseSchedule
        fields = ("id", "start_time", "end_time", "area")

    area = ma.Nested(AreaSchema)
    
class Course(db.Model):
    __tablename__="course"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=True)
    credits = db.Column(db.Integer, nullable=True, default=0)
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id')) 
    semester = db.Column(db.Integer,  nullable=True) 
    no_periods = db.Column(db.Integer,  nullable=True) 
    mandatory = db.Column(db.Boolean, default=False)
    course_schedule = db.relationship('CourseSchedule', back_populates='course')
    course_teacher = db.relationship('CourseTeacher', back_populates='course')

class CourseSchema(ma.Schema):
    class Meta:
        model = Course
        fields = ("id", "name", "code","semester","no_periods","mandatory", "course_schedule")
    course_schedule = ma.List(ma.Nested(CourseScheduleSchema))


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

class CourseTeacher(db.Model):
    __tablename__="course_teacher"
    id = db.Column(db.BIGINT, primary_key=True)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course.id'))
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher.id'))
    priority = db.Column(db.Integer, nullable=False)

    teacher = db.relationship('Teacher', back_populates='courses')
    course = db.relationship('Course',back_populates='course_teacher')

class CourseAssignments(db.Model):
    __tablename__="course_assignment"
    id = db.Column(db.BIGINT, primary_key=True)
    code = db.Column(db.String(10), nullable=True)
    no_students = db.Column(db.Integer, nullable=False)


class CourseScheduleOP(db.Model):
    __tablename__="course_schedule_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course_oc.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area_oc.id'),nullable=True) 
    

    course = db.relationship('CourseOP', back_populates='course_schedule')

class CourseScheduleOPSchema(ma.Schema):
    class Meta:
        model = CourseScheduleOP
        fields = ("id", "start_time", "end_time", "area")

    area = ma.Nested(AreaOPSchema)


class CourseOP(db.Model):
    __tablename__="course_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=True)
    credits = db.Column(db.Integer, nullable=True)
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id')) 
    semester = db.Column(db.Integer,  nullable=True) 
    no_periods = db.Column(db.Integer,  nullable=True) 
    no_students = db.Column(db.Integer,  nullable=True) 
    mandatory = db.Column(db.Boolean, default=False)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))

    course_schedule = db.relationship('CourseScheduleOP', back_populates='course')
    schedule = db.relationship('Schedule', back_populates='courses')
    assignment = db.relationship('Assignment', back_populates='course')
    course_teachers = db.relationship('CourseTeacherOP', back_populates='course')

    assigned = False

class CourseOPSchema(ma.Schema):
    class Meta:
        model = CourseOP
        fields = ("id", "name", "code","semester","no_periods","mandatory", "course_schedule")
    course_schedule = ma.List(ma.Nested(CourseScheduleOPSchema))


course_op_schema = CourseOPSchema()
courses_op_schema = CourseOPSchema(many=True)

class CourseTeacherOP(db.Model):
    __tablename__="course_teacher_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course_oc.id'))
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher_oc.id'))
    priority = db.Column(db.Integer, nullable=False)
    

    teachers = db.relationship('TeacherOP', back_populates='courses')
    course = db.relationship('CourseOP', back_populates='course_teachers')
