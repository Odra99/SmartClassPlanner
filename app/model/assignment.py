from app.extensions import db,ma
from app.model.course import CourseOPSchema
from app.model.teacher import TeacherOPSchema
from app.model.classE import ClassOPSchema
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
    teacher = db.relationship('TeacherOP', back_populates='assignment')
    classroom = db.relationship('ClassOP', back_populates='assignment')
    schedule = db.relationship('Schedule', back_populates='assignments')

class AssignmentSchema(ma.Schema):
    class Meta:
        model=Assignment
        fields = ("id", "name","course","teacher","classroom","start_time","end_time","no_students","section")
    course=ma.Nested(CourseOPSchema(exclude=("course_schedule",)))
    teacher=ma.Nested(TeacherOPSchema(exclude=("teacher_schedule",)))
    classroom = ma.Nested(ClassOPSchema(exclude=("class_schedule",)))

assignment_op_schema = AssignmentSchema()
assignments_op_schema = AssignmentSchema(many=True)