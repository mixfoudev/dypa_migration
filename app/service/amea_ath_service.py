from flask import current_app
from app.service import student_service as s
from app.service import static_data_service as staticService
from app import util as u
import uuid

def save2(user, contact, personal, student, classStud):
    eduId = staticService.get_edu_id(student.get('edu'))
    eduSpecId = staticService.get_edu_year_spec(student.get('edu'), classStud.get('acYear'), classStud.get('spec'))

    if not eduId or not eduSpecId:
        print(f"amea ath save: can not find eduId : {eduId} or eduSpecId: {eduSpecId}. Aborting")

    userId = s.getOrInsertUser(user)
    contactId = s.createContact(contact)
    personalId = s.createPersonal(personal)
    print("user id: ", userId)
    print("contact id: ", contactId)
    print("personal id: ", personalId)
    srUuid = str(uuid.uuid4())
    fieldsId = s.createStudentFields(student, userId, contactId, personalId, 1, eduSpecId, eduId, srUuid)
    print("fieldsId : ", fieldsId)

def save(user, contact, personal, student, classStud):
    db = current_app.config['DB']
    dypaId = 95
    try:
        # db.ping(reconnect=True)              # keep-alive (safe)
        # db.autocommit(False)                 # IMPORTANT: manual commit mode
        # db.begin()
        
        eduId = staticService.get_edu_id(student.get('edu'))
        eduSpec = staticService.get_edu_year_spec(student.get('edu'), classStud.get('acYear'), classStud.get('spec'))
        inputAcYearId = staticService.get_acYear_id(classStud.get('acYear'))
        section = staticService.get_class_section_id(dypaId, classStud.get('section'), 2, inputAcYearId)
        classId = section['id']
        print("classId", classId)
        inputAcYearId = section['academic_year_id']
        teachPeriodId = section['teach_period_id']
        periodNum = section['period_num']
        #print("periodNum", periodNum)

        if not eduId or not eduSpec or not classId:
            print(f"amea ath save: can not find eduId : {eduId} or eduSpec: {eduSpec} or classid: {classId} . Aborting")
            return False
        
        eduSpecId = eduSpec['id']
        with db.cursor() as cursor:
            userId = s.getOrInsertUser(user, cursor)
            if not userId:raise RuntimeError("userId failed")
            print("user id: ", userId)
            contactId = s.createContact(contact, cursor)
            if not contactId:raise RuntimeError("contactId failed")
            print("contact id: ", contactId)
            personalId = s.createPersonal(personal, cursor)
            if not personalId:raise RuntimeError("personalId failed")
            print("personal id: ", personalId)
            srUuid = str(uuid.uuid4())
            healthId = s.createHealth(student, cursor)
            if not healthId:raise RuntimeError("healthId failed")
            print("healthId id: ", healthId)
            fieldsId = s.createStudentFields(student, userId, healthId, contactId, personalId, dypaId, eduSpecId, eduId, srUuid, cursor)
            if not fieldsId:raise RuntimeError("fieldsId failed")
            print("fieldsId : ", fieldsId)
            stUuid = str(uuid.uuid4())
            studentId = s.createStudent(student, userId, contactId, eduSpecId, eduId, personalId, dypaId, fieldsId, stUuid, srUuid, cursor)
            if not studentId:raise RuntimeError("studentId failed")
            print("studentId : ", studentId)
            classStudId = s.createClassStudent(classStud, studentId, inputAcYearId, classId, teachPeriodId ,cursor)
            if not classStudId:raise RuntimeError("classStudId failed")
            print("classStudId : ", classStudId)
            classLessons = staticService.get_class_lessons(classId)
            s.createClassStudentLessons(classLessons, studentId, classStudId, periodNum, dypaId, cursor)
        db.commit()
        return True
    except Exception as e:
        #db.rollback()
        print("❌ Transaction failed:", e)
        return False
    