from app.extensions import db

class Course(db.Model):
    __tablename__="course"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id')) 
    semester = db.Column(db.Integer,  nullable=True) 
    no_periods = db.Column(db.Integer,  nullable=False) 
    schedule = db.relationship('CourseSchedule', backref='course')

class CourseSchedule(db.Model):
    __tablename__="course_schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id')) 

class CourseTeacher(db.Model):
    __tablename__="course_teacher"
    id = db.Column(db.BIGINT, primary_key=True)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course.id'))
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher.id'))
    priority = db.Column(db.Integer, nullable=False)

class CourseOP(db.Model):
    __tablename__="course_op"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id')) 
    semester = db.Column(db.Integer,  nullable=True) 
    no_periods = db.Column(db.Integer,  nullable=False) 
    schedule = db.relationship('CourseScheduleOP', backref='course')

class CourseScheduleOP(db.Model):
    __tablename__="course_schedule_op"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course_op.id'))
    area_id = db.Column(db.BIGINT,  db.ForeignKey('area.id')) 



class CourseTeacherOP(db.Model):
    __tablename__="course_teacher_op"
    id = db.Column(db.BIGINT, primary_key=True)
    course_id = db.Column(db.BIGINT,  db.ForeignKey('course_op.id'))
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher_op.id'))
    priority = db.Column(db.Integer, nullable=False)
    
