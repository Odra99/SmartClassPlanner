from app.extensions import db
from app.model.teacher import *
from app.model.course import CourseTeacher
from app.repository.course_repository import getCourseByCode
from app.ETL.generalFunctions import getDataFrame
from sqlalchemy import text

def etlTeacher(urlTeacher, urlTeacherSchedule, urlTeacherCourse):
    __truncateTeacher()
    dfTeacher = getDataFrame(urlTeacher)
    dfTeacherSchedule = getDataFrame(urlTeacherSchedule)
    dfTeacherCourse = getDataFrame(urlTeacherCourse)
    for i in range(len(dfTeacher)):
        schedule = __etlTeacherSchedule(
            dfTeacherSchedule, dfTeacher.iloc[i]['aux_id'])
        course = __etlTeacherCourse(
            dfTeacherCourse, dfTeacher.iloc[i]['aux_id'])
        aux = Teacher(name=dfTeacher.iloc[i]['name'])
        aux.teacher_schedule = schedule
        aux.courses = course
        db.session.add(aux)
    db.session.commit()


def __etlTeacherSchedule(df, aux_id):
    schedule = df[df["aux_id"] == aux_id]
    schedules = []
    for i in range(len(schedule)):
        aux = TeacherSchedule(start_time=schedule.iloc[i]['start_time'], end_time=schedule.iloc[i]['end_time'], area_id=int(
            schedule.iloc[i]['area_no']))
        schedules.append(aux)
    return schedules


def __etlTeacherCourse(df, aux_id):
    course = df[df["aux_id"] == aux_id]
    courses = []
    for i in range(len(course)):
        courseAux = getCourseByCode(str(course.iloc[i]['code']))
        if (courseAux is not None):
            aux = CourseTeacher(course_id=courseAux.id,
                                priority=int(course.iloc[i]['priority']))
            courses.append(aux)
    return courses


def __truncateTeacher():
    engine = db.engine
    table_name = 'teacher'
    truncate_query = text(f'''  TRUNCATE TABLE {table_name} CASCADE; ''')

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        connection.execute(truncate_query)
