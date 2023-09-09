from operator import itemgetter
from app.model.schedule import *
from app.model.assignment import *
from app.model.teacher import *
from app.model.classE import *
from app.model.course import *
from app.main.schedule.scheduleFunctions import *
from app.enums import RestrictionEnum,PriorityTypeEnum
from datetime import datetime,time,timedelta

def spaceAvailabilityCriteria(schedule:Schedule):
    classes= __sortClassPriority(schedule)
    courses = __sortCoursePriority(schedule)


    
def teacherAvailabilityCriteria(schedule:Schedule):
    classes = schedule.classes_configurations
    assignments=[]
    #period_duration_str = searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)
    period_duration = datetime.strptime(str("00:50"), '%H:%M').time()
    for teacher in schedule.teachers:
        for course in schedule.courses:
            if __isCourseAssigned(assignments,course):
                continue
            for teacherCourse in teacher.courses:
                if teacherCourse.course.code == course.code:
                    for teacherSchedule in teacher.teacher_schedule:
                        if(teacherSchedule.area_id == course.area_id):
                            teacherScheduleTime = datetime.strptime(str(teacherSchedule.start_time), '%H:%M:%S').time() 
                            teacherScheduleEndTime = datetime.strptime(str(teacherSchedule.end_time), '%H:%M:%S').time() 
                            notAvailable = False
                            while not __isTeacherAvailable(assignments,teacher,teacherScheduleTime) and teacherScheduleTime<teacherScheduleEndTime:
                                timedelta1 = timedelta(hours=teacherScheduleTime.hour,minutes=teacherScheduleTime.minute)
                                timedelta2 = timedelta(hours=period_duration.hour,minutes=period_duration.minute)
                                teacherScheduleTime = timedelta1 + (timedelta2)
                            
                            if(teacherScheduleTime>=teacherScheduleEndTime):
                                    notAvailable = True
                            if not notAvailable:
                                timedelta1 = timedelta(hours=teacherScheduleTime.hour,minutes=teacherScheduleTime.minute)
                                timedelta2 = timedelta(hours=period_duration.hour,minutes=period_duration.minute)
                                teacherScheduleEndTime = timedelta1 + (timedelta2 )
                                classE = classSpaceCriteria(classes,course,assignments,teacherScheduleTime)
                                if classE is not None:
                                    assignmentAuxiliar = Assignment(class_id=classE.id,course=course,teacher_id=teacher.id,schedule_id=schedule.id,start_time=teacherScheduleTime,end_time=teacherScheduleEndTime)
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
    

def __sortClassPriority(schedule:Schedule):
    attributes_to_order = ['space_capacity']
    space_capacity_pc = [pc for pc in schedule.priority_criterias if pc.subtype > PriorityTypeEnum.CLASS_SPACE_CAPACITY]
    if(len(space_capacity_pc)):
        return __custom_sort(schedule.classes_configurations,itemgetter(*attributes_to_order),reverse=space_capacity_pc[0].asc)    
    return __custom_sort(schedule.classes_configurations,itemgetter(*attributes_to_order))
    

def __sortCoursePriority(schedule:Schedule):
    course_pc = [pc for pc in schedule.priority_criterias if pc.type > PriorityTypeEnum.COURSE]
    #Order by subtype
    course_pc = sorted(course_pc,key=lambda pc : pc.order)
    attributes_to_order = []
    for pc in course_pc:
        if(pc.subtype==PriorityTypeEnum.COURSE_AREA):
            attributes_to_order.append('area_id')
        if(pc.subtype==PriorityTypeEnum.COURSE_NO_STUDENTS):
            attributes_to_order.append('no_students')
        if(pc.subtype==PriorityTypeEnum.COURSE_SEMESTER):
            attributes_to_order.append('semester')
    return __custom_sort(schedule.courses,itemgetter(*attributes_to_order))

    

def __areaPriority(schedule:Schedule):
    return sorted(schedule.area_configurations,key=lambda area : area.priority)

def __isTeacherAvailable(assignments: list[Assignment],teacher:TeacherOP, start_time):
    for assignment in assignments:
          if(teacher.id == assignment.teacher_id):
            start_time_a = datetime.strptime(str(assignment.start_time), '%H:%M:%S').time()
            end_time_a = datetime.strptime(str(assignment.end_time), '%H:%M:%S').time()
            start_time_t = datetime.strptime(str(start_time), '%H:%M:%S').time()
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

def __custom_sort(obj, key_func, reverse=False):
    return sorted(obj, key=key_func, reverse=reverse)
