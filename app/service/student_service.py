from csv import Error
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
        raise RuntimeError("[StudentService.createStudentFields] invalid dypaId: ", dypaId) 

def createStudent(dto, userId, contactId, eduSpecId, eduId, personalId, dypaId, fieldsId, uuid, srUuid, cursor=None):
    regDate = u.get_date(dto.get('dateRegister'))
    acYearId = staticService.get_acYear_id(dto.get('acYearRegister'))
    if dypaId in [33,95]: dypaId = 5

    skipGeneralLessons = 0
    if dypaId in [1,2] and dto.get('attendGeneralLesson') == 'ΟΧΙ': skipGeneralLessons = 1

    status = 'ACTIVE'
    kepeStatus=None
    gradDate=None
    if 'kepe' in dto.keys() and dto.get('kepe') == 'ΝΑΙ':
        status = 'GRADUATED'
        kepeStatus= 'ACTIVE'
        gradDate =  u.get_date(dto.get('gradDate'))
        # kepeDateReg = u.get_date(dto.get('dateRegister'))
        # regDate = None
    
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
    values.append(skipGeneralLessons) #skipGeneralLessons
    values.append(dto.get('social_id'))
    values.append(srUuid) ## srUuid
    values.append(status) #status
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
    values.append(kepeStatus)# kepeStatus
    values.append(gradDate) # graduation_date
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
    total_abs = (dto.get('abs') if dto.get('abs') else 0) + (dto.get('justAbs') if dto.get('justAbs') else 0)
    values.append(total_abs) # abs
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

def createPendingLessons(dto,  studId, eduId, specId, periodNum,cursor=None):
    lesIds = []
    perNums = []
    for i in range(1,5):
        k = 'pendLes'+str(i)
        if dto[k]:
            #print(k, ":", dto[k])
            lesIds.append(int(dto[k]))
            perNums.append(i)
    if len(lesIds) == 0: 
        print("no pending lessons found")
        return # return if no pending lessons found
    acYear = dto.get('acYearRegister')
    acYearId = staticService.get_acYear_id(acYear)
    acYearModel = staticService.get_ac_year(acYear)
    #print("acYearModel", acYearModel)
    prevYearId = None
    prevYearModel = None
    needsPrev = _needsPrevYear(periodNum, dto)
    if needsPrev:
        print("_needsPrevYear")
        acYearL = acYear.split("/")
        prevStr = f"{int(acYearL[0])-1}/{int(acYearL[1])-1}"
        prevYearModel = staticService.get_ac_year(prevStr)
        prevYearId = staticService.get_acYear_id(prevStr)
        if not prevYearId: raise Error("prevYearId is null")
        print(f"prev year= {prevYearId}:{prevStr}")
    
    print(f"creating {len(lesIds)} pending lessons")
    
    
    mod = periodNum % 2
    for i in range(0, len(lesIds)):
        year = acYearModel if not needsPrev or (perNums[i] % 2 == mod) else prevYearModel
        period = [p for p in year['periods'] if int(p['dypa_inst_type_id']) == 3 and int(p['num']) == perNums[i]][0]
        print(f"save acYearId= {acYearId}")
        print(f"save period= {period}")
        values = []
        values.append(eduId) # edu_id
        values.append(1) # is_pending
        values.append(lesIds[i]) # lesson_id
        values.append(perNums[i]) # period_num
        values.append(specId) # spec_id
        values.append(studId) # stud_group_id
        values.append(studId) # student_id
        values.append(None) # transfer_app_id
        values.append(None) # class_stud_lesson_id
        values.append(year['id']) # academic_year_id
        values.append(period['id']) # teach_period_id
        q.insert_pending_lesson(values,cursor)

def _needsPrevYear(periodNum, dto):
    if periodNum in [1,3] and (dto['pendLes1']or dto['pendLes3']): return True
    if periodNum in [2,4] and (dto['pendLes2']or dto['pendLes4']): return True
    return False