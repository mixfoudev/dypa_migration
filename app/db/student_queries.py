from flask import current_app

# def log_session(cursor, where):
#     cursor.execute("SELECT CONNECTION_ID() AS cid, @@autocommit AS ac")
#     row = cursor.fetchone()           # e.g., {'cid': 12345, 'ac': 0}
#     print(f"[{where}] conn_id={row['cid']}, autocommit={row['ac']}")

def get_user_by_vat(vat):
    db = current_app.config['DB']
    with db.cursor() as cursor:
        sql = "SELECT * FROM users WHERE vat = %s"
        cursor.execute(sql, (vat,)) 
        return cursor.fetchone()
    
def insert_user(values, cursor=None):
    sql = """INSERT INTO users (created_at, date_of_birth, father_lastname, father_name,firstname, gender, is_active, lastname, mother_lastname, mother_name, vat )
              VALUES (now(), %s, %s, %s,%s,%s,1,%s,%s,%s,%s)
            """
    if cursor:
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id

    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB User insert error:", e)
        return False
    
def insert_health(values, cursor=None):
    sql = """INSERT INTO health_info (
        created_at, updated_at, kepa_certificate_id
        )
        VALUES (now(), now(), %s)
        """
    print("Creating health_info with values: ",values)
    if cursor: 
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id
    
    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB health_info insert error:", e)
        return False
    
def insert_contact(values, cursor=None):
    sql = """INSERT INTO contact_details (
        created_at, updated_at, address, address_number, area, city, email,
        mobile, phone, postal_code, residence_regional_unit_id,residence_file_id, updated_by_user
        )
        VALUES (now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    print("Creating contact details with values: ",values)
    if cursor:
        print("cursor exists")  
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id
    print("cursor not exist. creating...")
    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB contact details insert error:", e)
        return False

def insert_personal(values, cursor=None):
    sql = """INSERT INTO personal_information (
            created_at, updated_at, amka, census_number, identity_number,
            municipality_of_registration, place_of_birth, amka_file_id,
            birth_regional_unit_id, country_id, identity_file_id,
            military_obligation_file_id, residence_permit_file_id, ama, bank_acc,
            male_reg_id, male_reg_place, citizenship, ama_file_id,
            unemployment_file_id, unemployment_months, bank_file_id,
            updated_by_user
            )
            VALUES (now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s)
            """
    print("Creating personal info with values: ",values)
    if cursor:
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id

    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB contact details insert error:", e)
        return False

def insert_student(values, cursor=None):
    #print(values)
    sql = """INSERT INTO students (
            created_at, updated_at, academic_year_id, am, comments, contact_details_id, 
            dypa_inst_type_id, edu_unit_id, edu_spec_id, eval_id, eval_uuid, exception, 
            ext_transfer_from, fields_id, personal_info_id, is_active, kpa, 
            practice_info_id, skip_general_lessons, social_id, sr_uuid, status, 
            transferred, type, uuid, doy_id, oral_file_id, stud_ex_reg_reason_id, 
            stud_ex_reg_sub_reason_id, register_education_id, submitter_id, user_id, 
            group_id, kepe_status, graduation_date, graduation_kepe_date, guardian_id, 
            remove_date, remove_reason, remove_file_id, register_date, is_migration
            )
            VALUES (now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    if cursor:
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        cursor.execute("UPDATE students SET group_id = %s WHERE id = %s", (new_id, new_id))
        return new_id

    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
            cursor.execute("UPDATE students SET group_id = %s WHERE id = %s", (new_id, new_id))
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB Student insert error:", e)
        return False
    
def insert_class_student_student(values, cursor=None):
    #print(values)
    sql = """INSERT INTO class_students (
            created_at, updated_at, academic_year_id, class_id, ext_name, is_active,
            student_id, teach_period, student_group_id, is_partial, classes_after,
            after_class_num, abs, just_abs, version, avg_grade, is_current, mig_abs,
            mig_just_abs, mig_avg_grade, mig_study_times
            )
            VALUES (now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s)
            """
    print("Creating class student with values: ",values)
    if cursor:
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id
    
    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB Class Student insert error:", e)
        return False
    
def insert_class_student_student_lessons(values, cursor=None):
    sql = """
            INSERT INTO class_student_lessons (
                created_at, updated_at, abs_passed, dypa_inst_type_id,
                exam1, exam2, exam_grade, exam_lab1, exam_lab2, exam_lab_grade,
                grades_passed, is_active, is_complete, is_current,
                lesson_id, oral1, oral2, oral_avg, oral_ex, oral_grade,
                oral_lab1, oral_lab2, oral_lab_avg, oral_lab_ex, oral_lab_grade,
                period_num, prog_grade, prog_lab_grade, student_id,
                total_grade, total_lab, total_theory, work_grade, work_lab_grade,
                class_lesson_id, class_student_id, abs, version
            )
            VALUES (
                now(), now(), %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
    if cursor:
        cursor.executemany(sql, values)
        return True
    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.executemany(sql, values)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print("❌ DB Class Student insert error:", e)
        return False
    
def insert_epas_registration(values, dypaId, cursor=None):
    if dypaId == 1:
        sql = """INSERT INTO student_epas_registrations (
            created_at, updated_at, date_submitted, eval_result, eval_status, status, uuid, academic_year_id,
            contact_details_id, dypa_inst_type_id, guardian_id, guardian_file_id,
            invitation_id, personal_info_id, social_id, register_education_id,
            user_id, reg_type
            )
            VALUES (
            now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """ 
    else:
        sql = """INSERT INTO student_pepas_registrations (
            created_at, updated_at, date_submitted, eval_result, eval_status, status, uuid, academic_year_id,
            contact_details_id, dypa_inst_type_id, guardian_id, guardian_file_id,
            invitation_id, personal_info_id, social_id, register_education_id,
            user_id, reg_type
            )
            VALUES (
            now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """ 
        #print("sql:", sql)
    if cursor:
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id

    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB epas/pepas student reg insert error:", e)
        return False
    
def insert_saek_registration(values, cursor=None):
    sql = """INSERT INTO student_saek_registrations (
            created_at, updated_at, status, uuid, academic_year_id,
            contact_details_id, personal_info_id, social_id, register_education_id,
            user_id, date_submitted, eval_result, eval_status, dypa_inst_type_id,
            invitation_id, reg_type
            )
            VALUES (
            now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
    if cursor:
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id
    
    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB Saek student reg insert error:", e)
        return False
    
def insert_amea_registration(values, cursor=None):
    sql = """INSERT INTO student_amea_registrations (
            created_at, updated_at, academic_year_id, date_submitted, dypa_inst_type_id,
            edu_id, edu_spec_id, eval_result, eval_status, status, uuid,
            contact_details_id, guardian_id, health_info_id, invitation_id,
            personal_info_id, social_id, register_education_id, user_id,
            guardian_file_id, edu_spec2_id, reg_type
            )
            VALUES (
            now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
            )
            """
    if cursor:
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id
    
    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB Amea student reg insert error:", e)
        return False
    

def insert_pending_lesson(values, cursor=None):
    sql = """INSERT INTO `student_transfer_pending_lessons` (`created_at`, `updated_at`, `edu_id`, `is_pending`, `lesson_id`, `period_num`, `spec_id`,
      `student_group_id`, `student_id`, `trasfer_app_id`, `class_student_lesson_id`, `academic_year_id`, `teach_period_id`)
        VALUES (now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    print("Creating pending lesson with values: ",values)
    if cursor:
        print("cursor exists")  
        cursor.execute(sql, (values))
        new_id = cursor.lastrowid
        return new_id
    print("cursor not exist. creating...")
    db = current_app.config['DB']
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (values))
            new_id = cursor.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        print("❌ DB pending lesson insert error:", e)
        return False