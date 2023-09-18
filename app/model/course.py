from app.extensions import db,ma
from app.model.general import AreaSchema, AreaOPSchema

class CourseSchedule(db.Model):
    __tablename__="course_schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course.id'))


    course = db.relationship('Course', back_populates='course_schedule')

class CourseScheduleSchema(ma.Schema):
    class Meta:
        model = CourseSchedule
        fields = ("id", "start_time", "end_time")


    
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
    area = db.relationship('Area', back_populates='courses')
    area_name=""

class CourseSchema(ma.Schema):
    class Meta:
        model = Course
        fields = ("id", "name", "code","semester","no_periods","mandatory", "course_schedule","area_name","area")
    course_schedule = ma.List(ma.Nested(CourseScheduleSchema))
    area = ma.Nested(AreaSchema)
    area_name = ma.Function(lambda area:(area.area.name))


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)



class CourseAssignments(db.Model):
    __tablename__="course_assignment"
    id = db.Column(db.BIGINT, primary_key=True)
    code = db.Column(db.String(10), nullable=True)
    no_students = db.Column(db.Integer, nullable=False)

class CourseAssignmentsSchema(ma.Schema):
    class Meta:
        model = CourseAssignments
        fields = ("id", "no_students", "code")


course_assignment_schema = CourseAssignmentsSchema()
courses_assignments_schema = CourseAssignmentsSchema(many=True)

class CourseAssignmentsOP(db.Model):
    __tablename__="course_assignment_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    code = db.Column(db.String(10), nullable=True)
    no_students = db.Column(db.Integer, nullable=False)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))


    schedule = db.relationship('Schedule', back_populates='course_assignment')

class CourseAssignmentsSchemaOP(ma.Schema):
    class Meta:
        model = CourseAssignmentsOP
        fields = ("id", "no_students", "code")


course_assignment_op_schema = CourseAssignmentsSchemaOP()
courses_assignments_op_schema = CourseAssignmentsSchemaOP(many=True)


class CourseScheduleOP(db.Model):
    __tablename__="course_schedule_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course_oc.id'))
    

    course = db.relationship('CourseOP', back_populates='course_schedule')

class CourseScheduleOPSchema(ma.Schema):
    class Meta:
        model = CourseScheduleOP
        fields = ("id", "start_time", "end_time")




class CourseOP(db.Model):
    __tablename__="course_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=True)
    credits = db.Column(db.Integer, nullable=True)
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area_oc.id')) 
    semester = db.Column(db.Integer,  nullable=True) 
    no_periods = db.Column(db.Integer,  nullable=True) 
    no_students = db.Column(db.Integer,  nullable=True) 
    mandatory = db.Column(db.Boolean, default=False)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))

    course_schedule = db.relationship('CourseScheduleOP', back_populates='course')
    schedule = db.relationship('Schedule', back_populates='courses')
    assignment = db.relationship('Assignment', back_populates='course')
    course_teacher = db.relationship('CourseTeacherOP', back_populates='course')
    area = db.relationship('AreaOp', back_populates='courses')

    assigned = False
    area_name=""

class CourseOPSchema(ma.Schema):
    class Meta:
        model = CourseOP
        fields = ("id", "name", "code","semester","no_periods","mandatory", "course_schedule","area_name","area")
    course_schedule = ma.List(ma.Nested(CourseScheduleOPSchema))
    area = ma.Nested(AreaOPSchema)


course_op_schema = CourseOPSchema()
courses_op_schema = CourseOPSchema(many=True)

class CourseTeacherOP(db.Model):
    __tablename__="course_teacher_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course_oc.id'))
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher_oc.id'))
    area_id = db.Column(db.BIGINT, db.ForeignKey('area_oc.id'))
    priority = db.Column(db.Integer, nullable=False)
    

    teachers = db.relationship('TeacherOP', back_populates='courses')
    course = db.relationship('CourseOP', back_populates='course_teacher')
    area = db.relationship('AreaOp', back_populates='area_teachers_course')

    code=""
    area_name=""

class CourseTeacherOPSchema(ma.Schema):
    class Meta:
        model = CourseTeacherOP
        fields = ("area_name","id","area",  "priority","code","course")
    area = ma.Nested(AreaOPSchema)
    course = ma.Nested(CourseOPSchema)

class CourseTeacher(db.Model):
    __tablename__="course_teacher"
    id = db.Column(db.BIGINT, primary_key=True)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course.id'))
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher.id'))
    priority = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.BIGINT, db.ForeignKey('area.id'))

    teacher = db.relationship('Teacher', back_populates='courses')
    course = db.relationship('Course',back_populates='course_teacher')
    area = db.relationship('Area', back_populates='area_teachers_course')
    area_name=""

class CourseTeacherSchema(ma.Schema):
    class Meta:
        model = CourseTeacher
        fields = ("id", "area_name", "priority","course","area")
    area = ma.Nested(AreaSchema)
    area_name = ma.Function(lambda area:(area.area.name))
    course = ma.Nested(CourseSchema)