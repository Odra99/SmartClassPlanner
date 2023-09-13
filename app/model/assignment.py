from app.extensions import db

class Assignment(db.Model):
    __tablename__="assignment"
    id = db.Column(db.BIGINT, primary_key=True)
    course_id = db.Column(db.BIGINT, db.ForeignKey('course_oc.id'))
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teacher_oc.id'))
    class_id = db.Column(db.BIGINT, db.ForeignKey('class_oc.id'))
    day = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    schedule_id = db.Column(db.BIGINT, db.ForeignKey('schedule.id'))
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    no_students = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(4), nullable=False)


    course = db.relationship('CourseOP', back_populates='assignment')
    schedule = db.relationship('Schedule', back_populates='assignments')

