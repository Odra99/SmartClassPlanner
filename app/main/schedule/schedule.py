from app.model.schedule import *
from app.main.schedule.scheduleFunctions import *
from app.enums import RestrictionEnum
import datetime

def scheduleGeneration(schedule:Schedule):
    


def __PeriodsAvailables(schedule:Schedule):
    start_time = searchRestriction(schedule.restrictions,RestrictionEnum.SCHEDULE_START_TIME)
    end_time = searchRestriction(schedule.restrictions,RestrictionEnum.SCHEDULE_END_TIME)
    period_duration =searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)
    no_periods_for_lunch = searchRestriction(schedule.restrictions, RestrictionEnum.NO_PERIODS_FOR_LUNCH)

    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')

    total_time = end - start

    no_peridos = (total_time / 60 / period_duration) - int(no_periods_for_lunch)
    return no_peridos


    



