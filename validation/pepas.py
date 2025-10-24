import pandas as pd
import re
from app.service import static_data_service as staticService

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

def calc_period(tp):
    if not tp: return None
    if tp.upper() in ["Α", "Α'", "Α ΤΆΞΗ", "Α ΤΑΞΗ"]: return 1
    if tp.upper() in ["Β", "Β'", "Β ΤΆΞΗ", "Β ΤΑΞΗ"]: return 2
    return None

def check_academic_years(df):
    ac = df['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].unique().tolist()
    reg = df['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].unique().tolist()
    un = list(set(ac + reg))
    ac_years = [s for s in un if validate_ac_year(s)]
    #ac_years.sort()
    # print(ac)
    # print(reg)
    # print(ac_years)
    out = []
    for ac in ac_years:
        exist = staticService.get_ac_year(ac)
        if not exist:
            out.append({"name": ac, "exist": False,  "periods": 0})
        else:
            if not exist['periods']:
                out.append({"name": ac, "exist": True,  "periods": 0})
            else:
                tp = [s for s in exist['periods'] if s['dypa_inst_type_id'] == dypaId]
                out.append({"name": ac, "exist": True, "periods": len(tp)})
    #print("ac yeaaaaaaaaaaars: ", out)
    return out

def is_valid_date(value):
    try:
        #splitter = "-" if "-" in value else "/"
        splitter = "/"
        dayFirst = len(value.split(splitter)[-1]) == 4
        if not dayFirst: return False
        pd.to_datetime(value, dayfirst=dayFirst, errors='raise')
        return True
    except Exception as e:
        print(e)
        return False

def validate_ac_year(value):
    try:
        start, end = value.split("/")
        if len(start) != 4 or len(end) != 4: return False
        if int(start) >= int(end) : return False
        if not (int(start) +1) == int(end) : return False
        return True
    except:
        return False

def isNumber(value, fun=float):
    try:
        fun(value)
        return True
    except:
        return False

def validate_field(row, field_name, value, err):
    if field_name == "ΑΜ":
        return pd.notna(value) and isNumber(value, int)
    
    if field_name == "ΑΔΤ":
        return pd.notna(value) and len(str(value)) > 5

    if field_name == "ΑΦΜ":
        return pd.notna(value) and isinstance(value, (int, float, str)) and str(value).isdigit() and len(str(value)) == 9

    if field_name == "ΑΜ":
        return pd.notna(value) and isinstance(value, (int, float, str)) and str(value).isdigit() and len(str(value)) >0

    elif field_name == "EMAIL":
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return pd.notna(value) and bool(re.match(pattern, str(value)))

    elif field_name in ["ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ"]:
        return pd.notna(value) and is_valid_date(value)

    elif field_name == "ΦΥΛΟ":
        return pd.notna(value) and str(value).strip().lower() in ["α", "θ"]

    elif field_name == "ΤΚ":
        return pd.notna(value) and str(value).isdigit() and len(str(value)) == 5
    
    elif field_name == "ΕΙΔΙΚΟΤΗΤΑ":
        return pd.notna(value) and staticService.spec_exists(dypaId, value)
    
    elif field_name == "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ":
        return pd.notna(value) and staticService.class_section_exists(dypaId, value, row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'])
    
    elif field_name in ["ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ"]:
        try:
            return pd.notna(value) and validate_ac_year(value)
        except Exception as e:
            return False

    elif field_name == "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ":
        return pd.notna(value) and value in ['ΝΑΙ', 'ΟΧΙ']

    # epas specific
    if field_name == "ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ":
        if "ΤΑΞΗ" in err: return False
        if calc_period(row['ΤΑΞΗ']) == 1: return True
        return pd.notna(value) and isNumber(value) and 9.5 < float(value) <= 20
    
    if field_name == "ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ":
        return pd.notna(value) and isNumber(value, int) and 0 <= int(value) < 2

    elif field_name == "ΤΑΞΗ":
        return pd.notna(value) and calc_period(value) in [1,2]
    
    elif field_name == "ΣΧΟΛΗ":
        return pd.notna(value) and staticService.edu_exists(dypaId, value)
    
    elif field_name == "ΧΩΡΑ":
        return pd.notna(value) and staticService.country_exists(value)

    return True

def update_row_data_info(row, students,section_students, err):
    print("erreeeeeeeeeeeeeeeeeee",err)
    print("dypaId",dypaId)
    for s in ['ΑΦΜ', 'ΟΝΟΜΑ', 'ΕΠΩΝΥΜΟ', 'ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']:
        if s in err: return
    vat = row['ΑΦΜ']
    name = row['ΟΝΟΜΑ']
    lastname = row['ΕΠΩΝΥΜΟ']
    sec = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']
    acYear = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']
    if not sec in section_students.keys(): section_students[sec] = {"name":sec,"total": 0, "exist": False, "data": []}
    section_students[sec]['data'].append(vat)
    section_students[sec]['exist'] = staticService.class_section_exists(dypaId, sec, acYear)
    students["data"].append({"vat":vat, "lastname":lastname, "name":name})

def eduSpecMissing(row, err):
    for s in ['ΕΙΔΙΚΟΤΗΤΑ', 'ΣΧΟΛΗ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']: 
        if s in err: True
    eduSpecId = staticService.get_edu_year_spec(row['ΣΧΟΛΗ'].strip(), row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'], row['ΕΙΔΙΚΟΤΗΤΑ'].strip())
    return eduSpecId is None

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
    unique_vats = []
    unique_adts = []
    unique_ams = {}
    students = {"total": 0, "data": []}
    section_students = {}
    row_errors={}
    existing_students = []
    
    for i, row in df.iterrows():
        err = []
        key = i+2
        if not key in row_errors: row_errors[key] = []

        for field in COLUMNS:
            if field not in row: continue
            val = row[field]
            if type(val) == str: val = val.strip()
            if not validate_field(row ,field, val, err):
                err.append(field)
                row_errors[key].append(field)    
            #print(f"{field}: {row[field]}")
        update_row_data_info(row, students, section_students, err)
        if "ΑΦΜ" not in err:
            vat = row['ΑΦΜ']
            if vat not in unique_vats:
                unique_vats.append(vat)
                if staticService.student_exists_by_vat(vat):
                    existing_students.append(vat)
            else: row_errors[key].append("Διπλότυπος ΑΦΜ")
        if "ΑΜ" not in err and 'ΣΧΟΛΗ' not in err:
            am = row['ΑΜ']
            sxoli = row['ΣΧΟΛΗ']
            if not sxoli in unique_ams.keys(): unique_ams[sxoli] = []
            if am not in unique_ams[sxoli]:
                unique_ams[sxoli].append(am)
            else: row_errors[key].append("Διπλότυπος ΑΜ για την σχολή " + sxoli)
            #
            if int(am) in staticService.get_edu_ams(dypaId, sxoli):
                row_errors[key].append("Ο ΑΜ υπάρχει στο σύστημα για την σχολή " + sxoli)
        if "ΑΔΤ" not in err:
            adt = row['ΑΔΤ']
            if adt not in unique_adts:
                unique_adts.append(adt)
            else: row_errors[key].append("Διπλότυπο ΑΔΤ")
        if (eduSpecMissing(row, err)):
            row_errors[key].append("ΕΙΔΙΚΟΤΗΤΑ ΑΝΑ ΕΤΟΣ")

    students["total"] = len(students["data"])
    for k in section_students:
        section_students[k]['total'] = len(section_students[k]['data'])


    for rk in row_errors.keys():
        if len(row_errors[rk]) == 0 : continue
        errors.append(f"Σειρά: {rk} - Μη έγκυρες τιμές: {', '.join(row_errors[rk])}")
    
    students['data'] = sorted(students["data"], key=lambda x: x['lastname'])
    data = {"errors": errors,"section_students": section_students,"students": students if len(students['data']) > 0 else None}
    acYears = check_academic_years(df)
    data['ac_years'] = sorted(acYears, key=lambda x: x['name'])
    data['existing_students'] = existing_students
    print("data", data)
    return data

# if __name__ == "__main__":
#     errors = validate_excel("data/epas.xlsx") 
#     if len(errors) == 0:
#         print("Everything seems ok.")
#     else:
#         for err in errors: print(err)
