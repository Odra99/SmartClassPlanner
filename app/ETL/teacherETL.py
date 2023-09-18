from app.extensions import db
from app.model.teacher import *
from app.model.course import CourseTeacher
from app.repository.course_repository import getCourseByCode
from app.ETL.generalFunctions import getDataFrame,searchAreaByName,truncateTable

def etlTeacher(urlTeacher, urlTeacherSchedule, urlTeacherCourse,areas):
    truncateTable('teacher')
    dfTeacher = getDataFrame(urlTeacher)
    dfTeacherSchedule = getDataFrame(urlTeacherSchedule)
    dfTeacherCourse = getDataFrame(urlTeacherCourse)
    for i in range(len(dfTeacher)):
        schedule = __etlTeacherSchedule(
            dfTeacherSchedule, dfTeacher.iloc[i]['aux_id'],areas)
        course = __etlTeacherCourse(
            dfTeacherCourse, dfTeacher.iloc[i]['aux_id'],areas)
        aux = Teacher(name=dfTeacher.iloc[i]['name'])
        aux.teacher_schedule = schedule
        aux.courses = course
        db.session.add(aux)
    db.session.commit()


def __etlTeacherSchedule(df, aux_id,areas):
    schedule = df[df["aux_id"] == aux_id]
    schedules = []
    for i in range(len(schedule)):
        area = searchAreaByName(areas,schedule.iloc[i]['area_name'])
        if(area is not None):   
            aux = TeacherSchedule(start_time=schedule.iloc[i]['start_time'], end_time=schedule.iloc[i]['end_time'], area_id=area.id)
            schedules.append(aux)
    return schedules


def __etlTeacherCourse(df, aux_id,areas):
    course = df[df["aux_id"] == aux_id]
    courses = []
    for i in range(len(course)):
        courseAux = getCourseByCode(str(course.iloc[i]['code']))
        if (courseAux is not None):
            area = searchAreaByName(areas,course.iloc[i]['area_name'])
            if(area is not None):  
                aux = CourseTeacher(course_id=courseAux.id,
                                priority=int(course.iloc[i]['priority']),
                                             area_id=area.id)
            courses.append(aux)
    return courses


