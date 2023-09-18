from app.model.schedule import *
from app.model.assignment import *
from app.model.teacher import *
from app.model.classE import *
from app.model.course import *
from app.main.schedule.scheduleFunctions import *
from app.enums import RestrictionEnum, PriorityTypeEnum


def generateAssignmentsBy(schedule:Schedule):
    return spaceAvailabilityCriteria(schedule)

def spaceAvailabilityCriteria(schedule: Schedule):
    __sortClassPriority(schedule)
    __sortCoursePriority(schedule)

    for priority_criteria in schedule.priority_criterias:
        if(priority_criteria.type==PriorityTypeEnum.CLASS.value):
            return classCriteria(schedule)
        if(priority_criteria.type==PriorityTypeEnum.TEACHER.value):
            return teacherCriteria(schedule)
        if(priority_criteria.type==PriorityTypeEnum.COURSE.value):
            return courseCriteria(schedule)

def courseCriteria(schedule: Schedule):
    classes = schedule.classes_configurations
    db.session.autoflush = False
    assignments = []
    period_duration_str = searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)
    if(period_duration_str is None):
        period_duration_str = "00:50"
    period_duration = transformTimeDelta(str(period_duration_str), '%H:%M')
   
    for course in schedule.courses:
        if __isCourseAssigned(assignments, course):
            continue
        for teacher in schedule.teachers:
            for teacherCourse in teacher.courses:
                if teacherCourse.course.code == course.code:
                    for teacherSchedule in teacher.teacher_schedule:
                        if (teacherSchedule.area_id == course.area_id):
                            teacherScheduleTime = transformTimeDelta(
                                str(teacherSchedule.start_time), '%H:%M:%S')
                            teacherScheduleEndTime = transformTimeDelta(
                                str(teacherSchedule.end_time), '%H:%M:%S')
                            notAvailable = False
                            while not __isTeacherAvailable(assignments, teacher, teacherScheduleTime) and teacherScheduleTime < teacherScheduleEndTime:
                                teacherScheduleTime = teacherScheduleTime+period_duration
                            if (teacherScheduleTime >= teacherScheduleEndTime):
                                notAvailable = True
                            if not notAvailable:
                                teacherScheduleEndTime = teacherScheduleTime + \
                                    (period_duration)
                                classE = classSpaceCriteria(
                                    classes, course, assignments, teacherScheduleTime)
                                if classE is not None:
                                    assignmentAuxiliar = Assignment(class_id=classE.id, course=course, teacher_id=teacher.id, no_students=10, section="1",
                                                                    schedule_id=schedule.id, start_time=teacherScheduleTime, end_time=teacherScheduleEndTime)
                                    assignments.append(assignmentAuxiliar)

                        break
                    break
    schedule.assignments = assignments
    db.session.commit()
    return schedule 

def classCriteria(schedule: Schedule):
    db.session.autoflush = False
    assignments = []
    period_duration_str = searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)
    if(period_duration_str is None):
        period_duration_str = "00:50"
    period_duration = transformTimeDelta(str(period_duration_str), '%H:%M')
    
    for classe in schedule.classes_configurations:
        for course in schedule.courses:
            if __isCourseAssigned(assignments, course):
                continue
            for teacher in schedule.teachers:
                for teacherCourse in teacher.courses:
                    if teacherCourse.course.code == course.code:
                        for teacherSchedule in teacher.teacher_schedule:
                            if (teacherSchedule.area_id == course.area_id):
                                teacherScheduleTime = transformTimeDelta(
                                    str(teacherSchedule.start_time), '%H:%M:%S')
                                teacherScheduleEndTime = transformTimeDelta(
                                    str(teacherSchedule.end_time), '%H:%M:%S')
                                notAvailable = False
                                while not __isTeacherAvailable(assignments, teacher, teacherScheduleTime) and teacherScheduleTime < teacherScheduleEndTime:
                                    teacherScheduleTime = teacherScheduleTime+period_duration
                                if (teacherScheduleTime >= teacherScheduleEndTime):
                                    notAvailable = True
                                if not notAvailable:
                                    teacherScheduleEndTime = teacherScheduleTime + \
                                        (period_duration)
                                    if __isClassAvailable(assignments,classe,teacherScheduleTime):
                                        classE = None 
                                        if (course.no_students > classe.space_capacity):
                                            course.no_students = course.no_students - classe.space_capacity
                                            classE = classe
                                        if classE is not None:
                                            assignmentAuxiliar = Assignment(class_id=classE.id, course=course, teacher_id=teacher.id, no_students=10, section="1",
                                                                        schedule_id=schedule.id, start_time=teacherScheduleTime, end_time=teacherScheduleEndTime)
                                            assignments.append(assignmentAuxiliar)

                            break
                        break
    schedule.assignments = assignments
    db.session.commit()
    return schedule 



def teacherCriteria(schedule: Schedule):
    classes = schedule.classes_configurations
    db.session.autoflush = False
    assignments = []
    period_duration_str = searchRestriction(schedule.restrictions, RestrictionEnum.PERIODS_DURATION)
    if(period_duration_str is None):
        period_duration_str = "00:50"
    period_duration = transformTimeDelta(str(period_duration_str), '%H:%M')
    for teacher in schedule.teachers:
        for course in schedule.courses:
            if __isCourseAssigned(assignments, course):
                continue
            for teacherCourse in teacher.courses:
                if teacherCourse.course.code == course.code:
                    for teacherSchedule in teacher.teacher_schedule:
                        if (teacherSchedule.area_id == course.area_id):
                            teacherScheduleTime = transformTimeDelta(
                                str(teacherSchedule.start_time), '%H:%M:%S')
                            teacherScheduleEndTime = transformTimeDelta(
                                str(teacherSchedule.end_time), '%H:%M:%S')
                            notAvailable = False
                            while not __isTeacherAvailable(assignments, teacher, teacherScheduleTime) and teacherScheduleTime < teacherScheduleEndTime:
                                teacherScheduleTime = teacherScheduleTime+period_duration
                            if (teacherScheduleTime >= teacherScheduleEndTime):
                                notAvailable = True
                            if not notAvailable:
                                teacherScheduleEndTime = teacherScheduleTime + \
                                    (period_duration)
                                classE = classSpaceCriteria(
                                    classes, course, assignments, teacherScheduleTime)
                                if classE is not None:
                                    assignmentAuxiliar = Assignment(class_id=classE.id, course=course, teacher_id=teacher.id, no_students=10, section="1",
                                                                    schedule_id=schedule.id, start_time=teacherScheduleTime, end_time=teacherScheduleEndTime)
                                    assignments.append(assignmentAuxiliar)

                        break
                    break
    schedule.assignments = assignments
    db.session.commit()
    return schedule


def classSpaceCriteria(classes: list[ClassOP], course: CourseOP, assignments: list[Assignment], start_time):
    for classE in classes:
        if __isClassAvailable(assignments, classE, start_time):
            if (course.no_students > classE.space_capacity):
                course.no_students = course.no_students - classE.space_capacity
            return classE
    return None


def __sortClassPriority(schedule: Schedule):
    space_capacity_pc = [
        pc for pc in schedule.priority_criterias if pc.type == PriorityTypeEnum.CLASS.value]
    if (len(space_capacity_pc)):
        if(space_capacity_pc[0].subtype==PriorityTypeEnum.CLASS_SPACE_CAPACITY.value and len(space_capacity_pc)==1):
          schedule.classes_configurations.sort(key=lambda x: (x.space_capacity))


def __sortCoursePriority(schedule: Schedule):
    course_pc = [
        pc for pc in schedule.priority_criterias if pc.type == PriorityTypeEnum.COURSE.value]
    # Order by subtype
    course_pc = sorted(course_pc, key=lambda pc: pc.order)
    attributes_to_order = []
    for pc in course_pc:
        if (pc.subtype == PriorityTypeEnum.COURSE_MANDATORY.value):
            attributes_to_order.append('mandatory')
        if (pc.subtype == PriorityTypeEnum.COURSE_NO_STUDENTS.value):
            attributes_to_order.append('no_students')
        if (pc.subtype == PriorityTypeEnum.COURSE_SEMESTER.value):
            attributes_to_order.append('semester')
    
    if(attributes_to_order[0]=='semester'):
      schedule.courses.sort(key=lambda x: (x.no_students is None, x.semester,x.mandatory))
    elif(attributes_to_order[0]=='no_students'):
      schedule.courses.sort(key=lambda x: (x.no_students is None, x.mandatory,x.semester))
    elif(attributes_to_order[0]=='mandatory'):
      schedule.courses.sort(key=lambda x: (x.mandatory is None, x.mandatory,x.semester,))


def __areaPriority(schedule: Schedule):
    return sorted(schedule.area_configurations, key=lambda area: area.priority)


def __isTeacherAvailable(assignments: list[Assignment], teacher: TeacherOP, start_time):
    for assignment in assignments:
        if (teacher.id == assignment.teacher_id):
            start_time_a = transformTimeDelta(
                str(assignment.start_time), '%H:%M:%S')
            end_time_a = transformTimeDelta(
                str(assignment.end_time), '%H:%M:%S')
            start_time_t = transformTimeDelta(
                str(start_time), '%H:%M:%S')
            if (start_time_a == start_time_t):
                return False
            if (start_time > start_time_a and start_time <= end_time_a):
                return False
    return True


def __isCourseAssigned(assignments: list[Assignment], course: CourseOP):
    for assignment in assignments:
        if (assignment.course_id == course.id):
            return course.assigned
    return False


def __isClassAvailable(assignments: list[Assignment], classE: ClassOP, start_time):
    for assignment in assignments:
        if (classE.id == assignment.class_id):
            start_time_a = transformTimeDelta(
                str(assignment.start_time))
            end_time_a = transformTimeDelta(
                str(assignment.end_time))
            start_time_t = transformTimeDelta(str(start_time))
            if (start_time_a == start_time_t):
                return False
            if (start_time > start_time_a and start_time < end_time_a):
                return False
    return True


def __isCourseAssignedForSameAreaAndSemester(assignments: list[Assignment], course: CourseOP, start_time):
    for assignment in assignments:
        if assignment.start_time == start_time:
            if assignment.course.semester == course.semester and assignment.course.area_id == course.area_id:
                return True
    return False



