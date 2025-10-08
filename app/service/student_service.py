from app.db import queries as sq
from app.db import student_queries as q
from app.service import static_data_service as staticService
from app import util as u


def getOrInsertUser(dto,cursor=None):
    vat = dto.get('vat')
    existed = q.get_user_by_vat(vat)
    if existed: 
        print("Fetched user with id: ", existed['id'])
        return existed['id']
    
    print("Creating user with vat: ", vat)
    values = []
    values.append(u.get_date(dto.get("dob")))
    values.append(dto.get('flastname'))
    values.append(dto.get('fname'))
    values.append(dto.get('name'))
    values.append(u.get_gender(dto.get('gender')))
    values.append(dto.get('lastname'))
    values.append(dto.get('mlastname'))
    values.append(dto.get('mname'))
    values.append(dto.get('vat'))
    return q.insert_user(values,cursor)

def createHealth(dto,cursor=None):
    values = []
    kepa = dto.get('kepa')
    hid = 1
    if kepa == 'ΛΟΙΠΕΣ ΟΡΓΑΝΙΚΕΣ ΠΑΘΗΣΕΙΣ': hid = 2
    elif kepa == 'ΨΥΧΙΚΕΣ ΠΑΘΗΣΕΙΣ': hid = 3
    elif kepa == 'ΚΙΝΗΤΙΚΗ ΑΝΑΠΗΡΙΑ 50%+': hid = 4
    values.append(hid)
    return q.insert_health(values,cursor)

def createContact(dto,cursor=None):
    values = []
    values.append(dto.get('address'))
    values.append(dto.get('addressNum'))
    values.append(dto.get('area'))
    values.append(dto.get('city'))
    values.append(dto.get('email'))
    values.append(dto.get('mobile'))
    values.append(dto.get('phone'))
    values.append(dto.get('zipcode'))
    values.append(dto.get('residence_regional_unit_id'))#
    values.append(dto.get('residence_file_id'))#
    values.append(0) # updated_by_user
    return q.insert_contact(values,cursor)

def createPersonal(dto,cursor=None):
    values = []
    values.append(dto.get('amka'))
    values.append(dto.get('cencusNum'))
    values.append(dto.get('identity'))
    values.append(dto.get('munRegister'))
    values.append(dto.get('birthPlace'))
    values.append(dto.get('amka_file_id'))
    values.append(dto.get('birth_regional_unit_id'))
    values.append(staticService.get_country_id(dto.get('country')))
    values.append(dto.get('identity_file_id'))
    values.append(dto.get('military_obligation_file_id'))
    values.append(dto.get('residence_permit_file_id'))
    values.append(dto.get('ama'))
    values.append(dto.get('iban'))
    values.append(dto.get('maleRegId'))
    values.append(dto.get('makeRegPlace'))
    values.append(dto.get('citizenship'))
    values.append(dto.get('ama_file_id'))
    values.append(dto.get('unemployment_file_id'))
    values.append(dto.get('unemployment_months'))
    values.append(dto.get('bank_file_id'))
    values.append(0) # updated_by_user
    return q.insert_personal(values,cursor)

def createStudentFields(dto, userId, healthId, contactId, personalId, dypaId, eduSpecId, eduId, uuid,cursor=None):
    print("creating student fields for dypaID: ", dypaId)
    if dypaId in (1,2):
        return createStudentEpasFields(dto, userId, contactId, personalId, dypaId, uuid,cursor)
    elif dypaId == 3:
        return createStudentSaekFields(dto, userId, contactId, personalId, uuid,cursor)
    elif dypaId in [33,95]:
        dypaId = 5
        return createStudentAmeaFields(dto, userId, healthId, contactId, eduSpecId, eduId, personalId, uuid,cursor)
    else:
        raise RuntimeError("[StudentService.createStudentFields] invalid dypaId") 

def createStudent(dto, userId, contactId, eduSpecId, eduId, personalId, dypaId, fieldsId, uuid, srUuid, cursor=None):
    regDate = u.get_date(dto.get('dateRegister'))
    acYearId = staticService.get_acYear_id(dto.get('acYearRegister'))
    if dypaId in [33,95]: dypaId = 5
    
    values = []
    values.append(acYearId) # acYearId
    values.append(dto.get('am'))
    values.append(dto.get('comments'))
    values.append(contactId)
    values.append(dypaId)
    values.append(eduId) # eduId
    values.append(eduSpecId)
    values.append(dto.get('eval_id')) 
    values.append(dto.get('eval_uuid'))
    values.append(0) # exception
    values.append(dto.get('ext_transfer_from'))
    values.append(fieldsId) ### fields_id
    values.append(personalId)
    values.append(1) # is_active
    values.append(dto.get('kpa'))
    values.append(dto.get('practice_info_id'))
    values.append(None) #skipGeneralLessons
    values.append(dto.get('social_id'))
    values.append(srUuid) ## srUuid
    values.append('ACTIVE') #status
    values.append(0) #transferred
    values.append('MIGRATION') # type
    values.append(uuid) ## uuid
    values.append(dto.get('doy_id'))
    values.append(dto.get('oral_file_id'))
    values.append(dto.get('stud_ex_reg_reason_id'))
    values.append(dto.get('stud_ex_reg_sub_reason_id'))
    values.append(dto.get('register_education_id'))
    values.append(dto.get('submitter_id'))
    values.append(userId) # user_id
    values.append(dto.get('group_id')) ## todo update the same instance ??
    values.append(dto.get('kepe_status'))
    values.append(dto.get('graduation_date'))
    values.append(dto.get('graduation_kepe_date'))
    values.append(dto.get('guardian_id'))
    values.append(dto.get('remove_date'))
    values.append(dto.get('remove_reason'))
    values.append(dto.get('remove_file_id'))
    values.append(regDate) # register_date
    values.append(1) # is_migration
    return q.insert_student(values,cursor)

def createClassStudent(dto, studentId, acId, sectionId, teachPeriodId,cursor=None):
    values = []
    values.append(acId) # academic_year_id
    values.append(sectionId) # class_id
    values.append(dto.get('ext_name'))
    values.append(1) # is_active
    values.append(studentId) # student_id
    values.append(teachPeriodId) # teach_period
    values.append(studentId) # student_group_id
    values.append(0) # is_partial
    values.append(0) # classes_after
    values.append(dto.get('after_class_num'))
    # add also mig abs as initial abs
    values.append(dto.get('abs') if dto.get('abs') else 0) # abs
    values.append(dto.get('justAbs') if dto.get('justAbs') else 0) # just_abs
    # values.append(0) # abs
    # values.append(0) # just_abs
    values.append(1) # version
    values.append(dto.get('avg_grade'))
    values.append(1) # is_current
    values.append(dto.get('abs') if dto.get('abs') else 0) # mig_abs
    values.append(dto.get('justAbs') if dto.get('justAbs') else 0) # mig_just_abs
    #values.append(0) # mig_just_abs
    values.append(dto.get('grade')) # mig_avg_grade
    values.append(None) # mig_study_times
    return q.insert_class_student_student(values,cursor)

def createClassStudentLessons(classLessons, studentId, classStudentId, periodNum, dypaId,cursor=None):
    if dypaId in [33,95]: dypaId = 5
    values = [
                (
                    1, # l.get('abs_passed'),
                    dypaId, #l.get('dypa_inst_type_id'),
                    l.get('exam1'),
                    l.get('exam2'),
                    l.get('exam_grade'),
                    l.get('exam_lab1'),
                    l.get('exam_lab2'),
                    l.get('exam_lab_grade'),
                    0, #l.get('grades_passed'),
                    1, # l.get('is_active'),
                    0, #l.get('is_complete'),
                    1, #l.get('is_current'),
                    l.get('lesson_id'),
                    l.get('oral1'),
                    l.get('oral2'),
                    l.get('oral_avg'),
                    l.get('oral_ex'),
                    l.get('oral_grade'),
                    l.get('oral_lab1'),
                    l.get('oral_lab2'),
                    l.get('oral_lab_avg'),
                    l.get('oral_lab_ex'),
                    l.get('oral_lab_grade'),
                    periodNum, #l.get('period_num'),
                    l.get('prog_grade'),
                    l.get('prog_lab_grade'),
                    studentId, #l.get('student_id'),
                    l.get('total_grade'),
                    l.get('total_lab'),
                    l.get('total_theory'),
                    l.get('work_grade'),
                    l.get('work_lab_grade'),
                    l.get('id'),# class_lesson_id
                    classStudentId, #g.get('class_student_id'),
                    0, #g.get('abs'),
                    1  #g.get('version'),
                )
                for l in classLessons
            ]
    #
    q.insert_class_student_student_lessons(values,cursor)

## student registrations

def createStudentEpasFields(dto, userId, contactId, personalId, dypaId, uuid,cursor=None):
    values = []
    values.append(dto.get('date_submitted'))
    values.append(dto.get('eval_result'))
    values.append(dto.get('eval_status'))
    values.append(dto.get('status'))
    values.append(uuid)
    values.append(staticService.get_acYear_id(dto.get('acYearRegister'))) # academic_year_id
    values.append(contactId) # contact_details_id
    values.append(dypaId) # dypa_inst_type_id
    values.append(dto.get('guardian_id'))
    values.append(dto.get('guardian_file_id'))
    values.append(dto.get('invitation_id'))
    values.append(personalId) # personal_info_id
    values.append(dto.get('social_id'))
    values.append(dto.get('register_education_id'))
    values.append(userId) # user_id
    values.append('MIGRATION') # reg_type
    return q.insert_epas_registration(values, dypaId,cursor)

def createStudentSaekFields(dto, userId, contactId, personalId, uuid,cursor=None):
    values = []
    values.append(dto.get('status'))
    values.append(uuid) ## uuid
    values.append(staticService.get_acYear_id(dto.get('acYearRegister'))) # academic_year_id
    values.append(contactId) # contact_details_id
    values.append(personalId) # personal_info_id
    values.append(dto.get('social_id'))
    values.append(dto.get('register_education_id'))
    values.append(userId) # user_id
    values.append(dto.get('date_submitted'))
    values.append(dto.get('eval_result'))
    values.append(dto.get('eval_status'))
    values.append(3) # dypa_inst_type_id
    values.append(dto.get('invitation_id'))
    values.append('MIGRATION') # reg_type
    return q.insert_saek_registration(values, cursor)

def createStudentAmeaFields(dto, userId, healthId, contactId, eduSpecId, eduId, personalId, uuid,cursor=None):
    print("createStudentAmeaFields")
    values = []
    values.append(staticService.get_acYear_id(dto.get('acYearRegister'))) # academic_year_id
    values.append(dto.get('date_submitted'))
    values.append(5) # dypa_inst_type_id
    values.append(dto.get('edu_id'))
    values.append(dto.get('edu_spec_id'))
    values.append(dto.get('eval_result'))
    values.append(dto.get('eval_status'))
    values.append(dto.get('status'))
    values.append(uuid) ## uuid
    values.append(contactId) # contact_details_id
    values.append(dto.get('guardian_id'))
    values.append(healthId) ## todo - edw kati tha thelw mallon
    values.append(dto.get('invitation_id'))
    values.append(personalId) # personal_info_id
    values.append(dto.get('social_id'))
    values.append(dto.get('register_education_id'))
    values.append(userId) # user_id
    values.append(dto.get('guardian_file_id'))
    values.append(dto.get('edu_spec2_id'))
    values.append('MIGRATION') # reg_type
    return q.insert_amea_registration(values, cursor)