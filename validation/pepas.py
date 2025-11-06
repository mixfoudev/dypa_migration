import pandas as pd
import re
from app.service import static_data_service as staticService
from validation import general_validations as v

# expected columns
COLUMNS = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΤΑΞΗ", "ΕΙΔΙΚΟΤΗΤΑ",  "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ","ΑΔΤ",
    "ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ", "ΑΡ. ΔΗΜΟΤΟΛΟΓ", "ΧΩΡΑ", "IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ", "ΑΜ",
    "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
    #,"ΑΔΙΚ.ΑΠΟΥΣΙΕΣ","ΜΗ ΜΕΤΡ.ΑΠΟΥΣΙΕΣ","ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ","ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ"
    ,"ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ","ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ"
]

dypaId = 2
unique_vats = []
unique_adts = []
existing_students=[]
unique_ams = {}
students = {"total": 0, "data": []}
section_students = {}

def calc_period(tp):
    if not tp: return None
    if tp.upper() in ["Α", "Α'", "Α ΤΆΞΗ", "Α ΤΑΞΗ"]: return 1
    if tp.upper() in ["Β", "Β'", "Β ΤΆΞΗ", "Β ΤΑΞΗ"]: return 2
    return None

def validate_personal(row):
    col = ["ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ","ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ", "ΑΔΤ", "ΧΩΡΑ", 
    #,"ΑΜ ΑΡΡΕΝΩΝ","ΑΡ. ΔΗΜΟΤΟΛΟΓ","ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ","ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ", "IBAN", "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ"
    ]
    return v.validate_personal(row, col, students, existing_students, unique_vats, unique_adts)

def validate_student(row):
    col = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΤΑΞΗ", "ΕΙΔΙΚΟΤΗΤΑ", "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ", "ΑΜ",
    "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
    #,"ΑΔΙΚ.ΑΠΟΥΣΙΕΣ","ΜΗ ΜΕΤΡ.ΑΠΟΥΣΙΕΣ",
    ,"ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ" # "ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ",
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
        if field_name == "ΕΙΔΙΚΟΤΗΤΑ":
            valid = staticService.spec_exists(dypaId, value)
            if valid: spec = value

        elif field_name == "ΤΑΞΗ":
            period = calc_period(value)
            valid = period != None and period in [1,2]

        elif field_name == "ΣΧΟΛΗ":
            valid = staticService.edu_exists(dypaId, value)
            if valid: sxoli = value
    
        elif field_name == "ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ":
            valid = v.isNumber(value, int) and 0 <= int(value) < 2

        elif field_name in ["ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ"]:
            valid = v.is_valid_date(value)

        elif field_name == "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ":
            valid = value in ['ΝΑΙ', 'ΟΧΙ']

        elif field_name in ["ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ"]:
            valid = v.validate_ac_year(value) and staticService.get_ac_year(value)

        if not valid: err.append(field_name)


    sec_val = ['ΣΧΟΛΗ', 'ΤΑΞΗ', 'ΕΙΔΙΚΟΤΗΤΑ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ', 'ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']
    if all([s not in err for s in sec_val]):
        sec = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ'].strip()
        valid = staticService.class_section_exists(dypaId, sec, row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'], period, spec)
        if not valid: err.append("ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ")
        # edu year spec
        valid = not v.eduSpecMissing(row, err)
        if not valid: err.append("ΕΙΔΙΚΟΤΗΤΑ ΑΝΑ ΕΤΟΣ")

    if period and period == 2 :
        value = row['ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ']
        valid = pd.notna(value) and v.isNumber(value) and 9.5 <= float(value) <= 20
        if not valid: err.append('ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ')

    if "ΑΜ" not in err and 'ΣΧΟΛΗ' not in err:
        am = row['ΑΜ']
        if not sxoli in unique_ams.keys(): unique_ams[sxoli] = []
        if am not in unique_ams[sxoli]:
            unique_ams[sxoli].append(am)
        else: err.append("Διπλότυπος ΑΜ για την σχολή " + sxoli)
        #
        if int(am) in staticService.get_edu_ams(dypaId, sxoli):
            err.append("Ο ΑΜ υπάρχει στο σύστημα για την σχολή " + sxoli)
    
    if len(err) == 0:
        if not sec in section_students.keys(): section_students[sec] = {"name":sec,"total": 0, "exist": False, "data": []}
        section_students[sec]['data'].append(row['ΑΦΜ'])
        section_students[sec]['exist'] = True
    return err

def validate_excel(file_path):
    df = pd.read_excel(file_path, dtype=str)
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
        print("pers_error: ", pers_error)
        if len(pers_error) > 0:
            err += pers_error
            row_errors[key] += pers_error

        stud_error = validate_student(row)
        print("stud_error: ", stud_error)
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