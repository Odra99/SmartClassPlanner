from app.extensions import db
from app.model.classE import *
from app.ETL.generalFunctions import getDataFrame

def etlCLass(url,urlSchedule):
    dfClass = getDataFrame(url)
    dfClassSchedule=getDataFrame(urlSchedule)
    for i in range(len(dfClass)):
        schedule = __etlClassSchedule(dfClassSchedule,dfClass.iloc[i]['name'])
        aux = Class(name=dfClass.iloc[i]['name'],space_capacity=int(dfClass.iloc[i]['space_capacity']))
        aux.class_schedule = schedule
        db.session.add(aux)
    db.session.commit()

def __etlClassSchedule(df,name):    
    schedule = df[df["name"]==name]
    schedules = []
    for i in range(len(schedule)):
        aux = ClassSchedule(start_time=schedule.iloc[i]['start_time'],end_time=schedule.iloc[i]['end_time'],area_id=int(schedule.iloc[i]['area_no']))
        schedules.append(aux)
    return schedules
 