from app.extensions import db

class Teacher(db.Model):
    __tablename__="teacher"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    teacher_schedule = db.relationship('TeacherSchedule', back_populates='teacher')
    

class TeacherSchedule(db.Model):
    __tablename__="teacher_schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'),nullable=True)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher.id'))
    area_id = db.Column(db.Integer, nullable=False) 


    teacher = db.relationship('Teacher', back_populates='teacher_schedule')


class TeacherOP(db.Model):
    __tablename__="teacher_op"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))

    teacher_schedule = db.relationship('TeacherScheduleOP', back_populates='teacher')
    courses = db.relationship('CourseTeacherOP', back_populates='teachers')
    schedule = db.relationship('Schedule', back_populates='teachers')

class TeacherScheduleOP(db.Model):
    __tablename__="teacher_schedule_op"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher_op.id'))
    area_id = db.Column(db.Integer, nullable=False) 


    teacher = db.relationship('TeacherOP', back_populates='teacher_schedule')

