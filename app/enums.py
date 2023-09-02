from enum import Enum

class RestrictionEnum(Enum):
    NO_MAX_ASSIGNMENTS_PER_TEACHER=1
    NO_PERIODS_FOR_LUNCH=2
    SCHEDULE_START_TIME=3
    SCHEDULE_END_TIME=4
    PERIODS_DURATION=5
    NO_PERIODS=6
    MAX_NUMBER_OF_STUDENTS_PER_CLASS=7