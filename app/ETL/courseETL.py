from app.extensions import db
from app.model.course import *
from app.ETL.generalFunctions import getDataFrame

def etlCourse(urlCourse,urlCourseSchedule):
    dfCourse = getDataFrame(urlCourse)
    dfCourseSchedule=getDataFrame(urlCourseSchedule)
    for i in range(len(dfCourse)):
        schedule = __etlCourseSchedule(dfCourseSchedule,dfCourse.iloc[i]['code'])
        aux = Course(name=dfCourse.iloc[i]['name'],code=dfCourse.iloc['code'],semester=dfCourse.iloc['semester'],area_id=dfCourse.iloc['area_no'])
        aux.schedule = schedule
        db.session.add(aux)
    db.session.commit()

def __etlCourseSchedule(df,code):    
    schedule = df[df["code"]==code]
    schedules = []
    for i in range(len(schedule)):
        aux = CourseSchedule(start_time=schedule.iloc[i]['start_time'],end_time=schedule.iloc[i]['end_time'],area_id=int(schedule.iloc[i]['area_no']))
        schedules.append(aux)
    return schedules
 