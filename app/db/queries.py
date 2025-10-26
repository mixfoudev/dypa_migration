from flask import current_app

def get_users():
    db = current_app.config['DB']
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
def get_ams_for_edu(eduId):
    db = current_app.config['DB']
    with db.cursor() as cursor:
            cursor.execute(f"SELECT distinct am FROM students where edu_unit_id={eduId}")
            return cursor.fetchall()
    
def get_schools(dypaId):
    db = current_app.config['DB']
    print("DB. fetching schools for dypa: ", dypaId)
    if dypaId in [33,95]:
        if dypaId ==33: dypaId=3
        with db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM educational_units where id={dypaId}")
            return cursor.fetchall()
    else:
        with db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM educational_units where dypa_institution_type_id={dypaId}")
            return cursor.fetchall()

def get_student_specs(dypaId):
    db = current_app.config['DB']
    print("DB. fetching specs for dypa: ", dypaId)
    if dypaId in [33,95]:
        if dypaId ==33: dypaId=3
        with db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM student_specialties where edu_id={dypaId}")
            return cursor.fetchall()
    else:
        with db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM student_specialties where dypa_institution_type_id={dypaId}")
            return cursor.fetchall()
        
def get_student_period_lessons(specId, periodNum):
    db = current_app.config['DB']
    print(f"DB. fetching lessons spec:{specId} and period:{periodNum} ")
    with db.cursor() as cursor:
            cursor.execute(f"SELECT id FROM aa_lessons where student_specialty_id={specId} and period_num={periodNum}")
            return cursor.fetchall()
        
    
def get_edu_year_spec(eduId, acYearId, specId):
    db = current_app.config['DB']
    with db.cursor() as cursor:
        cursor.execute(f"""
                    select es.id from educational_unit_specialties es
                    inner join ac_year_student_specialties acs on acs.id = es.ac_year_student_specialty_id
                    where es.educational_unit_id = {eduId} and acs.academic_year_id = {acYearId} and es.student_specialty_id={specId};
                    """)
        return cursor.fetchone()
    
def get_class_sections(dypaId):
    db = current_app.config['DB']
    #print("DB. fetching specs for dypa: ", dypaId)
    if dypaId in [33,95]:
        if dypaId ==33: dypaId=3
        with db.cursor() as cursor:
            cursor.execute(f"SELECT cs.*, ac.name as 'acName' FROM class_sections cs inner join academic_years ac on ac.id = cs.academic_year_id where cs.edu_id={dypaId}")
            return cursor.fetchall()
    else:
        with db.cursor() as cursor:
            cursor.execute(f"SELECT cs.*, ac.name as 'acName' FROM class_sections cs inner join academic_years ac on ac.id = cs.academic_year_id where cs.dypa_inst_type_id={dypaId}")
            return cursor.fetchall()
    
def get_class_lessons(cId):
    db = current_app.config['DB']
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * from class_lessons where class_id = {cId}")
        return cursor.fetchall()    
    
def get_class_lessonsWithEpasLessonType(cId):
    db = current_app.config['DB']
    with db.cursor() as cursor:
        cursor.execute(f"SELECT cl.*, l.epas_lesson_type from class_lessons cl inner join aa_lessons l on l.id =cl.lesson_id where cl.class_id = {cId} ")
        return cursor.fetchall()
    
    
def get_countries():
    db = current_app.config['DB']
    print("DB. fetching countries")
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM countries")
        return cursor.fetchall()    
    
def get_academic_years():
    db = current_app.config['DB']
    print("DB. fetching ac years")
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM academic_years")
        return cursor.fetchall()
    
def get_academic_year_periods(acId):
    db = current_app.config['DB']
    #print(f"DB. fetching ac year id:{acId} periods ")
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM teach_periods where academic_year_id={acId}")
        return cursor.fetchall()
    
def active_student_exists_by_vat(vat):
    db = current_app.config['DB']
    with db.cursor() as cursor:
        cursor.execute(f"""select * from students s 
                        inner join users u on u.id = s.user_id
                        where s.is_active=1 and u.vat={vat}
                        """)
        return cursor.fetchall()