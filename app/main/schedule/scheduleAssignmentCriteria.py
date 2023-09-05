from app.model.schedule import *
from app.model.assignment import *
from app.model.teacher import *
from app.model.classE import *
from app.model.course import *
from app.main.schedule.scheduleFunctions import *
from app.enums import RestrictionEnum
import datetime

def __spaceAvailabilityCriteria(schedule:Schedule,no_periods):
      classes = schedule.classes

def teacherAvailabilityCriteria(schedule:Schedule):
    classes = schedule.classes
    assignments=[]
    period_duration_str = searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)
    period_duration = datetime.strptime(str(period_duration_str), '%H:%M').time()
    for teacher in schedule.teacher_configurations:
        for course in schedule.courses:
            if __isCourseAssigned(assignments,course):
                continue
            for teacherCourse in teacher.courses:
                if teacherCourse.code == course.code:
                    for teacherSchedule in teacher.schedule:
                        if(teacherSchedule.area_id == course.area_id):
                            teacherScheduleTime = datetime.strptime(str(teacherSchedule.start_time), '%H:%M').time() 
                            teacherScheduleEndTime = datetime.strptime(str(teacherSchedule.end_time), '%H:%M').time() 
                            notAvailable = False
                            while not __isTeacherAvailable(assignments,teacher,teacherScheduleTime):
                                teacherScheduleTime = teacherScheduleTime + period_duration
                                if(teacherScheduleTime==teacherScheduleEndTime):
                                    notAvailable = True
                            if not notAvailable:
                                teacherScheduleEndTime = teacherScheduleTime + period_duration
                                classE = classSpaceCriteria(classes)
                                assignmentAuxiliar = Assignment(course=course,teacher=teacher,schedule=schedule,start_time=teacherScheduleTime,end_time=teacherScheduleEndTime)
                                assignments.append(assignmentAuxiliar)
                        break
                    break


def classSpaceCriteria(classes:list[ClassOP],course:CourseOP,assignments: list[Assignment],start_time):
    for classE in classes:
        if  __isClassAvailable(assignments,classE,start_time):
            if(course.no_students>classE.space_capacity):
                course.no_students = course.no_students - classE.space_capacity
            return classE
    return None
    

         

def __areaPriority(schedule:Schedule):
    return sorted(schedule.area_configurations,key=lambda area : area.priority)

def __isTeacherAvailable(assignments: list[Assignment],teacher:TeacherOP, start_time):
    for assignment in assignments:
          if(teacher.id == assignment.teacher_id):
            start_time_a = datetime.strptime(str(assignment.start_time), '%H:%M').time()
            end_time_a = datetime.strptime(str(assignment.end_time), '%H:%M').time()
            start_time_t = datetime.strptime(str(start_time), '%H:%M').time()
            if(start_time_a==start_time_t):
                return False
            if(start_time>start_time_a and start_time<=end_time_a):
                return False
    return True

def __isCourseAssigned(assignments: list[Assignment], course:CourseOP):
    for assignment in assignments:
        if(assignment.course_id==course.id):
            return course.assigned
    return False

def __isClassAvailable(assignments: list[Assignment], classE: ClassOP,start_time):
    for assignment in assignments:
          if(classE.id == assignment.class_id):
            start_time_a = datetime.strptime(str(assignment.start_time), '%H:%M').time()
            end_time_a = datetime.strptime(str(assignment.end_time), '%H:%M').time()
            start_time_t = datetime.strptime(str(start_time), '%H:%M').time()
            if(start_time_a==start_time_t):
                return False
            if(start_time>start_time_a and start_time<end_time_a):
                return False
    return True

def __isCourseAssignedForSameAreaAndSemester(assignments: list[Assignment], course: CourseOP,start_time):
    for assignment in assignments:
        if assignment.start_time == start_time:
            if assignment.course.semester == course.semester and assignment.course.area_id==course.area_id:
                return True
    return False