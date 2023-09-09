from app.model.schedule import *
from app.main.schedule.scheduleFunctions import *
from app.main.schedule.scheduleAssignmentCriteria import *
from app.enums import RestrictionEnum,StatusEnum
import datetime
from app.repository import *
from app.model import *
from app.extensions import db

def scheduleGeneration():
    schedule = schedule_repository.getInProgressSchedule()
    if schedule is None:
        schedule = Schedule(date=datetime.datetime.now(),version=1,status=StatusEnum.IN_PROGRESS.value)
        schedule.classes_configurations = __loadClasses()
        schedule.courses = __loadCourses()
        schedule.teachers = __loadTeacher(schedule.id)
        db.session.add(schedule)
        db.session.commit()
    teacherAvailabilityCriteria(schedule)
    

        

def __PeriodsAvailables(schedule:Schedule):
    start_time = searchRestriction(schedule.restrictions,RestrictionEnum.SCHEDULE_START_TIME)
    end_time = searchRestriction(schedule.restrictions,RestrictionEnum.SCHEDULE_END_TIME)
    period_duration =searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)

    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')

    total_time = end - start

    no_peridos = (total_time / 60 / period_duration)
    return no_peridos

def __loadClasses():
    classes = class_repository.getAll()
    print(classes)
    classesOC = []
    for classE in classes:
        auxClass = ClassOP(name=classE.name,space_capacity=int(classE.space_capacity))
        schedules = []
        for classSchedule in classE.class_schedule:
            aux = ClassScheduleOP(start_time=classSchedule.start_time,end_time=classSchedule.end_time)
            schedules.append(aux)
        auxClass.class_schedule = schedules
        classesOC.append(auxClass)
    return classesOC

def __loadCourses():
    courses = course_repository.getAllCourses()
    assingments = course_repository.getAllAssignment()
    coursesOC = []
    for course in courses:
        assingmenta = list(e for e in assingments if e.code  == course.code)
        auxCourse = CourseOP(name=course.name,code=str(course.code),semester=int(course.semester),no_periods=int(course.no_periods))
        if len(assingmenta)>0:
            assingment = assingmenta[0]
            auxCourse.no_students = assingment.no_students
        schedules = []
        for courseSchedule in course.course_schedule:
            aux = CourseScheduleOP(start_time=courseSchedule.start_time,end_time=courseSchedule.end_time)
            schedules.append(aux)
        auxCourse.course_schedule = schedules
        coursesOC.append(auxCourse)
    return coursesOC
    

def __loadTeacher(scheduleId):
    teachers = teacher_repository.getAllTeachers()
    teachersOC = []
    for teacher in teachers:
        auxTeacher = TeacherOP(name=teacher.name)
        schedules = []
        for teacherSchedule in teacher.teacher_schedule:
            aux = TeacherScheduleOP(start_time=teacherSchedule.start_time,end_time=teacherSchedule.end_time)
            schedules.append(aux)
        auxTeacher.teacher_schedule = schedules
        courses = []
        for course in teacher.courses:
            courseAux = course_repository.getCourseOPByCode(course.course.code, scheduleId)
            aux = CourseTeacherOP(course_id=courseAux.id,priority=course.priority)
            courses.append(aux)
        auxTeacher.courses = courses
        teachersOC.append(auxTeacher)
    return teachersOC
    




