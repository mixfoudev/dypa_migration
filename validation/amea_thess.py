import pandas as pd
from app.service import static_data_service as staticService
from validation import general_validations as v
from app import util as u

# expected columns
COLUMNS = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΕΤΟΣ", "ΠΑΘΗΣΗ ΚΕΠΑ", "ΕΙΔΙΚΟΤΗΤΑ",  "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ", "ΥΠΗΚΟΟΤΗΤΑ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ","ΑΔΤ","IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΑΜ","ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ", "ΚΕΠΕ",
    "ΗΜΝΙΑ ΑΠΟΦΟΙΤΗΣΗΣ"
]

dypaId = 33
unique_vats = []
unique_adts = []
existing_students=[]
unique_ams = {}
students = {"total": 0, "data": []}
section_students = {}
kepas = ["ΚΩΦΩΣΗ", "ΛΟΙΠΕΣ ΟΡΓΑΝΙΚΕΣ ΠΑΘΗΣΕΙΣ","ΨΥΧΙΚΕΣ ΠΑΘΗΣΕΙΣ", "ΚΙΝΗΤΙΚΗ ΑΝΑΠΗΡΙΑ 50%+", "ΤΥΦΛΟΤΗΤΑ", "ΝΟΗΤΙΚΗ ΥΣΤΕΡΗΣΗ", "ΣΥΝΔΡΟΜΑ", "ΑΥΤΙΣΜΟΣ", "ΜΑΘΗΣΙΑΚΕΣ ΔΥΣΚΟΛΙΕΣ"]

def validate_personal(row):
    col = ["ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΑΔΤ", "ΧΩΡΑ", "ΠΑΘΗΣΗ ΚΕΠΑ", "ΥΠΗΚΟΟΤΗΤΑ"
    #,"ΑΜ ΑΡΡΕΝΩΝ","ΑΡ. ΔΗΜΟΤΟΛΟΓ","ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ","ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ", "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ","IBAN", "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ"
    ]
    err = v.validate_personal(row, col, students, existing_students, unique_vats, unique_adts)
    field = 'ΠΑΘΗΣΗ ΚΕΠΑ'
    if field not in err:
        if str(row[field]).strip().upper() not in kepas:
            err.append(field)
    return err

def validate_student(row, prevErr):
    col = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΕΤΟΣ", "ΚΕΠΕ"
    ]
    err = []
    period = None
    spec = None
    sxoli = None
    sec = None

    for field_name in col:
        if field_name not in row: continue
        value = row[field_name]
        if type(value) == str: value = value.strip()
        #print(f"p val field: {field_name} | value: {value} | isna: {pd.isna(value)}")
        if pd.isna(value): 
            err.append(field_name)
            continue
        valid = True

        if field_name == "ΚΕΠΕ":
            valid = value in ['ΝΑΙ', 'ΟΧΙ']

        elif field_name == "ΕΤΟΣ":
            valid = 1 <= int(value) <= 5

        if not valid: err.append(field_name)
    
    if "ΚΕΠΕ" not in err:
        val = row["ΗΜΝΙΑ ΑΠΟΦΟΙΤΗΣΗΣ"]
        kepe = row['ΚΕΠΕ'] == 'ΝΑΙ'
        valid = pd.isna(val) if not kepe else pd.notna(val) and v.is_valid_date(val)
        if not valid: err.append('ΗΜΝΙΑ ΑΠΟΦΟΙΤΗΣΗΣ')

    allErr = err + prevErr
    sec_val = ['ΣΧΟΛΗ', 'ΕΙΔΙΚΟΤΗΤΑ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ', 'ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ', 'ΚΕΠΕ', 'ΕΤΟΣ']
    if all([s not in allErr for s in sec_val]):
        period = int(row['ΕΤΟΣ']) if row['ΚΕΠΕ']!='ΝΑΙ' else int(row['ΕΤΟΣ']) + 10
        sec = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ'].strip()
        spec = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
        sxoli = row['ΣΧΟΛΗ'].strip()
        valid = staticService.class_section_exists(dypaId, sec, row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'], period, spec, sxoli)
        if not valid:
            allErr.append("ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ")
            err.append("ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ")

    if sec and len(err) == 0:
        if not sec in section_students.keys(): section_students[sec] = {"name":sec,"total": 0, "exist": False, "data": []}
        if not row['ΑΦΜ'] in section_students[sec]['data']: section_students[sec]['data'].append(row['ΑΦΜ'])
        section_students[sec]['exist'] = True
    return err

def validate_excel(file_path):
    global unique_adts, unique_ams, unique_vats, existing_students, students, section_students
    unique_vats = []
    unique_adts = []
    existing_students=[]
    unique_ams = {}
    students = {"total": 0, "data": []}
    section_students = {}
    # df = pd.read_excel(file_path, dtype=str)
    df = u.load_excel(file_path)
    data = {"errors": None,"section_students": None,"students": None}

    errors = set(COLUMNS) - set(df.columns)
    if errors:
        r = [f"Δεν βρέθηκε η στήλη: {e}" for e in errors]
        #return r, None, None
        data["errors"] = r
        return data
    if df.shape[0] == 0:
        data["errors"] = ["Το αρχείο δεν έχει δεδομένα"]
        return data

    errors = []
    row_errors={}
    
    for i, row in df.iterrows():
        err = []
        key = i+2
        if not key in row_errors: row_errors[key] = []

        pers_error = validate_personal(row)
        #print("pers_error: ", pers_error)
        if len(pers_error) > 0:
            err += pers_error
            row_errors[key] += pers_error

        global_stud_error = v.validate_global_student(row, dypaId, unique_ams)
        #print("global_stud_error: ", global_stud_error)
        if len(global_stud_error) > 0:
            err += global_stud_error
            row_errors[key] += global_stud_error

        stud_error = validate_student(row, err)
        #print("stud_error: ", stud_error)
        if len(stud_error) > 0:
            err += stud_error
            row_errors[key] += stud_error

    students["total"] = len(students["data"])
    for k in section_students:
        section_students[k]['total'] = len(section_students[k]['data'])


    for rk in row_errors.keys():
        if len(row_errors[rk]) == 0 : continue
        errors.append(f"Σειρά: {rk} - Μη έγκυρες τιμές: {', '.join(row_errors[rk])}")
    
    students['data'] = sorted(students["data"], key=lambda x: x['lastname'])
    data = {"errors": errors,"section_students": section_students,"students": students if len(students['data']) > 0 else None}
    acYears = v.check_academic_years(df, dypaId)
    data['ac_years'] = sorted(acYears, key=lambda x: x['name'])
    data['existing_students'] = existing_students
    return data
