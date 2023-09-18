from app.extensions import db
from app.model.course import *
from app.ETL.generalFunctions import getDataFrame,searchAreaByName,truncateTable

def etlCourse(urlCourse,urlCourseSchedule,areas):
    truncateTable('course')
    dfCourse = getDataFrame(urlCourse)
    dfCourseSchedule=getDataFrame(urlCourseSchedule)
    for i in range(len(dfCourse)):
        schedule = __etlCourseSchedule(dfCourseSchedule,dfCourse.iloc[i]['code'])
        area = searchAreaByName(areas,dfCourse.iloc[i]['area_name'])
        if(area is not None):
            aux = Course(name=dfCourse.iloc[i]['name'],code=str(dfCourse.iloc[i]['code']),semester=int(dfCourse.iloc[i]['semester']), mandatory=bool(dfCourse.iloc[i]['mandatory']),area_id=area.id,no_periods=int(dfCourse.iloc[i]['no_periods']))
            aux.course_schedule = schedule
            db.session.add(aux)
    db.session.commit()

def __etlCourseSchedule(df,code):    
    schedule = df[df["code"]==code]
    schedules = []
    for i in range(len(schedule)):
        aux = CourseSchedule(start_time=str(schedule.iloc[i]['start_time']),end_time=str(schedule.iloc[i]['end_time']))
        schedules.append(aux)
    return schedules

def etlCourseAssignment(url):
    truncateTable('course_assignment')
    df = getDataFrame(url)
    for i in range(len(df)):
        aux = CourseAssignments(code=str(df.iloc[i]['code']),no_students=int(df.iloc[i]['no_students']))
        db.session.add(aux)
    db.session.commit()

