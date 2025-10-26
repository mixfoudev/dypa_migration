from flask import current_app
from app.service import student_service as s
from app.service import static_data_service as staticService
from app import util as u
import uuid

def save(user, contact, personal, student, classStud):
    db = current_app.config['DB']
    dypaId = 3
    try:
        eduId = staticService.get_edu_id(student.get('edu'))
        eduSpec = staticService.get_edu_year_spec(student.get('edu'), classStud.get('acYear'), classStud.get('spec'))
        section = staticService.get_class_section_id(dypaId, classStud.get('section'))
        classId = section['id']
        print("classId", classId)
        inputAcYearId = section['academic_year_id']
        teachPeriodId = section['teach_period_id']
        periodNum = section['period_num']
        #print("periodNum", periodNum)

        if not eduId or not eduSpec or not classId:
            print(f"saek save: can not find eduId : {eduId} or eduSpec: {eduSpec} or classid: {classId} . Aborting")
            return False
        
        eduSpecId = eduSpec['id']
        with db.cursor() as cursor:
            userId = s.getOrInsertUser(user, cursor)
            print("user id: ", userId)
            contactId = s.createContact(contact, cursor)
            print("contact id: ", contactId)
            personalId = s.createPersonal(personal, cursor)
            print("personal id: ", personalId)
            srUuid = str(uuid.uuid4())
            fieldsId = s.createStudentFields(student, userId, None, contactId, personalId, dypaId, eduSpecId, eduId, srUuid, cursor)
            print("fieldsId : ", fieldsId)
            stUuid = str(uuid.uuid4())
            studentId = s.createStudent(student, userId, contactId, eduSpecId, eduId, personalId, dypaId, fieldsId, stUuid, srUuid, cursor)
            print("studentId : ", studentId)
            classStudId = s.createClassStudent(classStud, studentId, inputAcYearId, classId, teachPeriodId ,cursor)
            print("classStudId : ", classStudId)
            classLessons = staticService.get_class_lessonsEpas(classId)
            # if student.get('attendGeneralLesson') == 'ΟΧΙ':
            #     classLessons = [l for l in classLessons if l['epas_lesson_type'] != 'GENERAL']
            s.createClassStudentLessons(classLessons, studentId, classStudId, periodNum, dypaId, cursor)
        db.commit()
        return True
    except Exception as e:
        #db.rollback()
        print("❌ Transaction failed:", e)
        return False
    