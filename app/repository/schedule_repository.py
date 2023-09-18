from app.extensions import db
from app.model.schedule import *
from app.model.assignment import Assignment
from app.enums import StatusEnum, RestrictionEnum
from app.main.schedule.scheduleFunctions import searchRestriction, transformTimeDelta
import numpy as np
import pandas as pd
from collections import OrderedDict


def getInProgressSchedule():
    schedule = db.session.query(Schedule).filter_by(
        parent_id=None, status=StatusEnum.IN_PROGRESS.value).first()
    schedule.matrixAssingments = __matrixGenerator(schedule)
    return schedule


def __matrixGenerator(schedule: Schedule):
    times = __PeriodsAvailables(schedule)
    classrooms = schedule.classes_configurations
    assignmentMatrix = np.ndarray(
        (int(len(times)), int(len(classrooms))), dtype=Assignment)
    assignments = schedule.assignments
    columns = __pandasColumns(classrooms)
    indexN = __pandasIndex(times)
    for assignment in assignments:
        i = 0
        for classroom in classrooms:
            if assignment.classroom.id == classroom.id:
                index = __findStartTime(times, assignment.start_time)
                if (index is not None):
                    assignmentMatrix[index][i] = {
                        "course": assignment.course.name, "teacher": assignment.teacher.name, "no_students": assignment.no_students,"id":assignment.id,"section":assignment.section}
                    break
            i = i + 1
    df = pd.DataFrame(assignmentMatrix, columns=columns, index=indexN)
    return  df[columns].to_dict(orient='index') 


def __pandasColumns(classrooms):
    columns = []
    for classroom in classrooms:
        columns.append(classroom.name)
    return columns


def __pandasIndex(times):
    index = []
    for time in times:
        index.append(time['start']+"-"+time['end'])
    return index


def __findStartTime(times, timeH):
    i = -1
    timestr = str(transformTimeDelta(timeH))
    for time in times:
        i = i + 1
        if (time['start'] == timestr):
            return i

    return None


def __PeriodsAvailables(schedule: Schedule):
    start_time = searchRestriction(
        schedule.restrictions, RestrictionEnum.SCHEDULE_START_TIME)
    end_time = searchRestriction(
        schedule.restrictions, RestrictionEnum.SCHEDULE_END_TIME)
    period_duration = searchRestriction(
        schedule.restrictions, RestrictionEnum.PERIODS_DURATION)

    start = transformTimeDelta(start_time)
    end = transformTimeDelta(end_time)
    period_duration = transformTimeDelta(period_duration, '%H:%M')

    total_time = end - start

    no_peridos = (total_time / period_duration)

    classTimes = []

    i = 0
    while i < no_peridos:
        aux = start
        start = start + (period_duration)
        i = i+1
        hoursAux, remainderAux = divmod(aux.seconds, 3600)
        minutesAux, secondsAux = divmod(remainderAux, 60)
        hours, remainder = divmod(start.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        classTimes.append({"start": f"{hoursAux:02d}:{minutesAux:02d}:{secondsAux:02d}",
                          "end": f"{hours:02d}:{minutes:02d}:{seconds:02d}"})
    return classTimes
