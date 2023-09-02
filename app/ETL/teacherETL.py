from app.extensions import db
from app.model.teacher import *
from app.ETL.generalFunctions import getDataFrame

def etlTeacher(urlTeacher,urlTeacherSchedule):
    dfTeacher = getDataFrame(urlTeacher)
    dfTeacherSchedule=getDataFrame(urlTeacherSchedule)
    for i in range(len(dfTeacher)):
        schedule = __etlTeacherSchedule(dfTeacherSchedule,dfTeacher.iloc[i]['aux_id'])
        aux = Teacher(name=dfTeacher.iloc[i]['name'])
        aux.schedule = schedule
        db.session.add(aux)
    db.session.commit()

def __etlTeacherSchedule(df,aux_id):    
    schedule = df[df["aux_id"]==aux_id]
    schedules = []
    for i in range(len(schedule)):
        aux = TeacherSchedule(start_time=schedule.iloc[i]['start_time'],end_time=schedule.iloc[i]['end_time'],area_id=int(schedule.iloc[i]['area_no']))
        schedules.append(aux)
    return schedules
        

4