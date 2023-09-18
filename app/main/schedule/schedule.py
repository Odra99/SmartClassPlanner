from app.model.schedule import *
from app.main.schedule.scheduleFunctions import *
from app.main.schedule.scheduleAssignmentCriteria import *
from app.enums import RestrictionEnum,StatusEnum
import datetime
from app.repository import schedule_repository,course_repository
from app.model import *
from app.extensions import db

def scheduleGeneration(schedule_dict):
    schedule = schedule_repository.getInProgressScheduleF()
    if schedule is None:
        schedule = Schedule(date=datetime.datetime.now(),version=1,status=StatusEnum.IN_PROGRESS.value)
    else:
        schedule = Schedule(date=datetime.datetime.now(),version=(schedule.version+1),status=StatusEnum.IN_PROGRESS.value,parent_id=schedule.id)
    db.session.add(schedule)
    db.session.commit()
    schedule.restrictions = __loadRestrictions(schedule_dict)
    schedule.priority_criterias = __loadPriorities(schedule_dict)
    schedule.areas = __loadAreas(schedule_dict)
    schedule.course_assignment = __loadCourseAssignment(schedule_dict)
    db.session.add(schedule)
    db.session.commit()
    schedule.classes_configurations = __loadClasses(schedule_dict,schedule.areas)
    schedule.courses = __loadCourses(schedule_dict,schedule.areas)
    schedule.teachers = __loadTeacher(schedule.id,schedule_dict,schedule.areas)
    db.session.add(schedule)
    db.session.commit()
    

        

def __PeriodsAvailables(schedule:Schedule):
    start_time = searchRestriction(schedule.restrictions,RestrictionEnum.SCHEDULE_START_TIME)
    end_time = searchRestriction(schedule.restrictions,RestrictionEnum.SCHEDULE_END_TIME)
    period_duration =searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)

    if(start_time is None):
        start_time="07:50:00"
    if(end_time is None):
        end_time="21:10:00"
    if(period_duration is None):
        period_duration = "00:50"
    start = transformTimeDelta(start_time)
    end = transformTimeDelta(end_time)
    period_duration = transformTimeDelta(period_duration,'%H:%M')

    total_time = end - start

    no_peridos = (total_time / 60 / period_duration)

    classTimes = []

    i = 0
    
    while i < no_peridos:
        aux = start
        start = start + (period_duration) 
        i=i+1
        classTimes.append({"start":str(aux),"end":str(start)})
    return classTimes


def __loadClasses(classes_dict,areas):
    classes = classes_dict['classes_configurations']
    classesOC = []
    for classE in classes:
        auxClass = ClassOP(name=classE['name'],space_capacity=int(classE['space_capacity']))
        schedules = []
        for classSchedule in classE['class_schedule']:
            aux = ClassScheduleOP(start_time=classSchedule['start_time'],end_time=classSchedule['end_time'])
            area = __searchAreaByName(areas,classSchedule['area_name'])
            if(area is not None):
                aux.area_id = area.id
            schedules.append(aux)
        auxClass.class_schedule = schedules
        classesOC.append(auxClass)
    return classesOC

def __loadRestrictions(schedule_dict):
    restrictions = schedule_dict['restrictions']
    restrictionsOC = []
    for restriction in restrictions:
        auxRestriction = ScheduleRestrictions(name=restriction['name'],value=restriction['value'])
        restrictionsOC.append(auxRestriction)
    return restrictionsOC

def __loadPriorities(schedule_dict):
    priorities = schedule_dict['priority_criterias']
    prioritiesOc = []
    for priority in priorities:
        auxRestriction = ScheduleConfigurationPriorityCriteria(description=priority['description'],type=int(priority['type']),subtype=int(priority['subtype']),order=int(priority['order']))
        prioritiesOc.append(auxRestriction)
    return prioritiesOc

def __loadAreas(schedule_dict):
    areas = schedule_dict['areas']
    areasAc = []
    for area in areas:
        auxArea = AreaOp(name=area['name'],color=area['color'])
        areasAc.append(auxArea)
    return areasAc

def __loadCourseAssignment(schedule_dict):
    assignments = schedule_dict['course_assignment']
    assignmentOc = []
    for assignment in assignments:
        auxArea = CourseAssignmentsOP(code=assignment['code'],no_students=int(assignment['no_students']))
        assignmentOc.append(auxArea)
    return assignmentOc

def __loadCourses(schedule_dict,areas):
    courses = schedule_dict['courses']
    assingments = schedule_dict['course_assignment']
    coursesOC = []
    for course in courses:
        assingmenta = list(e for e in assingments if e['code']  == course['code'])
        auxCourse = CourseOP(name=course['name'],code=str(course['code']),semester=int(course['semester']),no_periods=int(course['no_periods']),mandatory=course['mandatory'])
        area = __searchAreaByName(areas,course['area_name'])
        if(area is not None):
            auxCourse.area_id = area.id
        if len(assingmenta)>0:
            assingment = assingmenta[0]
            auxCourse.no_students = assingment['no_students']
        schedules = []
        for courseSchedule in course['course_schedule']:
            aux = CourseScheduleOP(start_time=courseSchedule['start_time'],end_time=courseSchedule['end_time'])
            schedules.append(aux)
        auxCourse.course_schedule = schedules
        coursesOC.append(auxCourse)
    return coursesOC
    

def __loadTeacher(scheduleId,schedule_dict,areas):
    teachers = schedule_dict['teachers']
    teachersOC = []
    for teacher in teachers:
        auxTeacher = TeacherOP(name=teacher['name'])
        schedules = []
        for teacherSchedule in teacher['teacher_schedule']:
            aux = TeacherScheduleOP(start_time=teacherSchedule['start_time'],end_time=teacherSchedule['end_time'])
            schedules.append(aux)
        auxTeacher.teacher_schedule = schedules
        courses = []
        for course in teacher['courses']:
            area = __searchAreaByName(areas,course['area_name'])
            courseAux = course_repository.getCourseOPByCode(course['code'], scheduleId,area.id)
            aux = CourseTeacherOP(course_id=courseAux.id,priority=course['priority'], area_id=area.id)
            courses.append(aux)
        auxTeacher.courses = courses
        teachersOC.append(auxTeacher)
    return teachersOC
    

def __searchAreaByName(areas,name):
    for area in areas:
        if(area.name==name):
            return area
    return None

