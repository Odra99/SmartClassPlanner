from app.extensions import db

class Teacher(db.Model):
    __tablename__="teacher"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    schedule = db.relationship('TeacherSchedule', backref='teacher')

class TeacherSchedule(db.Model):
    __tablename__="teacher_schedule"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'),nullable=True)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher.id'))
    area_id = db.Column(db.Integer, nullable=False) 


class TeacherOP(db.Model):
    __tablename__="teacher_op"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    schedule = db.relationship('TeacherScheduleOP', backref='teacher')
    assignments = db.relationship('Assignment', backref='teacher')

class TeacherScheduleOP(db.Model):
    __tablename__="teacher_schedule_op"
    id = db.Column(db.BIGINT, primary_key=True)
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher_op.id'))
    area_id = db.Column(db.Integer, nullable=False) 

