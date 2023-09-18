from app.model.schedule import *
from app.main.schedule.scheduleFunctions import *
from app.main.schedule.scheduleAssignmentCriteria import generateAssignmentsBy
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
    db.session.commit()
    schedule.classes_configurations = __loadClasses(schedule_dict,schedule.areas)
    schedule.courses = __loadCourses(schedule_dict,schedule.areas)
    schedule.teachers = __loadTeacher(schedule.id,schedule_dict,schedule.areas)
    db.session.commit()
    schedule = generateAssignmentsBy(schedule)
    schedule.matrixAssingments = matrixGenerator(schedule)
    schedule.efficiency = len(schedule.classes_configurations)*len(schedule.courses)/(len(schedule.assignments))
    db.session.commit()
    return schedule

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
            area = __searchAreaByName(areas,teacherSchedule['area_name'])
            if(area is not None):
                aux = TeacherScheduleOP(start_time=teacherSchedule['start_time'],end_time=teacherSchedule['end_time'],area_id=area.id)
                schedules.append(aux)
        auxTeacher.teacher_schedule = schedules
        courses = []
        for course in teacher['courses']:
            area = __searchAreaByName(areas,course['area_name'])
            if area is not None:
                course2 = course_repository.getCourseOPByid(course['id'])
                if(course2 is not None):
                    courseAux = course_repository.getCourseOPByCode(course2.code,scheduleId,area.id)
                    if(courseAux is not None):
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

