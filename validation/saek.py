import pandas as pd
import re
from app.service import static_data_service as staticService

# expected columns
COLUMNS = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΕΞΑΜΗΝΟ", "ΕΙΔΙΚΟΤΗΤΑ",  "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ","ΑΔΤ",
    "ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ", "ΑΡ. ΔΗΜΟΤΟΛΟΓ", "ΧΩΡΑ", "IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ","ΑΜ",
    "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
    ,"ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ"
]

pending_cols=["ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ"]

dypaId = 3
prev_years =[]

def calc_period(tp):
    if not tp: return None
    if tp.upper() in ["Α", "Α'", "Α ΕΞΑΜΗΝΟ", "Α ΕΞΆΜΗΝΟ"]: return 1
    if tp.upper() in ["Β", "Β'", "Β ΕΞΑΜΗΝΟ", "Β ΕΞΆΜΗΝΟ"]: return 2
    if tp.upper() in ["Γ", "Γ'", "Γ ΕΞΑΜΗΝΟ", "Γ ΕΞΆΜΗΝΟ"]: return 3
    if tp.upper() in ["Δ", "Δ'", "Δ ΕΞΑΜΗΝΟ", "Δ ΕΞΆΜΗΝΟ"]: return 4
    return None

def validate_pending_lesson(row, period):
    print("validate_pending_lesson period:", period)
    sameMsg = 'Δεν μπορεί να υπάρχει χρωστ. μάθημα στο ίδιο εξάμηνο πλήρους φοίτησης'
    upperMsg = 'Δεν μπορεί να υπάρχει χρωστ. μάθημα σε εξάμηνο μεγαλύτερο της πλήρους φοίτησης'
    if period is None: return "Μη έγκυρο εξάμηνο" # should never
    if period ==1: 
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']): return sameMsg
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']): return upperMsg
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ']): return upperMsg
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']): return upperMsg
    if period ==2: 
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']): return sameMsg
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ']): return upperMsg
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']): return upperMsg
    if period ==3: 
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ']): return sameMsg
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']): return upperMsg
    if period ==4: 
        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']): return sameMsg
    return None

def check_academic_years(df):
    ac = df['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].unique().tolist()
    reg = df['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].unique().tolist()
    un = list(set(ac + reg + prev_years))
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
        period = int(calc_period(row['ΕΞΑΜΗΝΟ']))
        return pd.notna(value) and staticService.class_section_exists(dypaId, value, row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'], period)
    
    elif field_name in ["ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ"]:
        try:
            return pd.notna(value) and validate_ac_year(value)
        except Exception as e:
            return False
    
    if field_name == "ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ":
        return pd.notna(value) and isNumber(value, int) and 0 <= int(value) < 2

    elif field_name == "ΕΞΑΜΗΝΟ":
        return pd.notna(value) and calc_period(value) in [1,2,3,4]
    
    elif field_name == "ΣΧΟΛΗ":
        return pd.notna(value) and staticService.edu_exists(dypaId, value)
    
    elif field_name == "ΧΩΡΑ":
        return pd.notna(value) and staticService.country_exists(value)
    
    elif field_name == "ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ":
        return pd.isna(value) or (isNumber(value, int) and staticService.lesson_exists(row['ΕΙΔΙΚΟΤΗΤΑ'], 1, value)) 
    
    elif field_name == "ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ":
        return pd.isna(value) or (isNumber(value, int) and staticService.lesson_exists(row['ΕΙΔΙΚΟΤΗΤΑ'], 2, value)) 
    
    elif field_name == "ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ":
        return pd.isna(value) or (isNumber(value, int) and staticService.lesson_exists(row['ΕΙΔΙΚΟΤΗΤΑ'], 3, value)) 
    
    elif field_name == "ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ":
        return pd.isna(value) or (isNumber(value, int) and staticService.lesson_exists(row['ΕΙΔΙΚΟΤΗΤΑ'], 4, value)) 

    return True

def update_row_data_info(row, students,section_students, err):
    for s in ['ΑΦΜ', 'ΟΝΟΜΑ', 'ΕΠΩΝΥΜΟ', 'ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']:
        if s in err: return
    vat = row['ΑΦΜ']
    name = row['ΟΝΟΜΑ']
    lastname = row['ΕΠΩΝΥΜΟ']
    sec = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']
    acYear = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']
    periodNum = calc_period(row['ΕΞΑΜΗΝΟ'])
    if not sec in section_students.keys(): section_students[sec] = {"name":sec,"total": 0, "exist": False, "data": []}
    section_students[sec]['data'].append(vat)
    section_students[sec]['exist'] = staticService.class_section_exists(dypaId, sec, acYear, int(periodNum))
    students["data"].append({"vat":vat, "lastname":lastname, "name":name})

def update_part_row_data_info(row, students, part_students, err):
    for s in ['ΑΦΜ', 'ΟΝΟΜΑ', 'ΕΠΩΝΥΜΟ', 'ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']:
        if s in err: return
    vat = row['ΑΦΜ']
    name = row['ΟΝΟΜΑ']
    lastname = row['ΕΠΩΝΥΜΟ']
    # sec = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']
    acYear = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']
    if not 'data' in part_students.keys(): part_students['data'] = []
    part_students['data'].append(vat)
    students["data"].append({"vat":vat, "lastname":lastname, "name":name})

def eduSpecMissing(row, err):
    for s in ['ΕΙΔΙΚΟΤΗΤΑ', 'ΣΧΟΛΗ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']: 
        if s in err: True
    eduSpecId = staticService.get_edu_year_spec(row['ΣΧΟΛΗ'], row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'], row['ΕΙΔΙΚΟΤΗΤΑ'])
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
    part_students = {}
    row_errors={}
    existing_students = []
    
    for i, row in df.iterrows():
        err = []
        #ownsLesson = pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])
        onlyPart = pd.isna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']) and pd.isna(row['ΕΞΑΜΗΝΟ']) and pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])
        print("onlyPart", onlyPart)
        key = i+2
        if not key in row_errors: row_errors[key] = []

        for field in COLUMNS:
            if field not in row: continue
            val = row[field]
            if type(val) == str: val = val.strip()
            if onlyPart and field in ['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ','ΕΞΑΜΗΝΟ']: continue
            if field == 'ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ' and pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']) and (pd.notna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']) or pd.notna(row['ΕΞΑΜΗΝΟ']) ):
                print("aaaaaaaaaaa")
                err.append(field)
                row_errors[key].append(field) 
                continue
            if not validate_field(row ,field, val, err):
                err.append(field)
                row_errors[key].append(field)    
        
        if not onlyPart and 'ΕΞΑΜΗΝΟ' not in err:
            period = calc_period(row['ΕΞΑΜΗΝΟ'])
            valError = validate_pending_lesson(row, period)
            if valError: row_errors[key].append(valError)
            else:
                # check prev years
                if 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ' not in err:
                    needsPrev = _needsPrevYear(period, row)
                    if needsPrev:
                        acYearL = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].split("/")
                        prevStr = f"{int(acYearL[0])-1}/{int(acYearL[1])-1}"
                        if prevStr not in prev_years: prev_years.append(prevStr)

        if onlyPart:
            period = 4
            # check prev years
            if 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ' not in err:
                needsPrev = _needsPrevYear(period, row)
                if needsPrev:
                    acYearL = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].split("/")
                    prevStr = f"{int(acYearL[0])-1}/{int(acYearL[1])-1}"
                    if prevStr not in prev_years: prev_years.append(prevStr)

        if onlyPart: update_part_row_data_info(row, students, part_students, err)
        else: update_row_data_info(row, students, section_students, err)
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
    data = {"errors": errors,"section_students": section_students,"students": students if len(students['data']) > 0 else None, "part_students": part_students}
    acYears = check_academic_years(df)
    data['ac_years'] = sorted(acYears, key=lambda x: x['name'])
    data['existing_students'] = existing_students
    return data

def _needsPrevYear(periodNum, row):
    if periodNum in [1,3] and (pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ'])): return True
    if periodNum in [2,4] and (pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])): return True
    return False

# if __name__ == "__main__":
#     errors = validate_excel("data/epas.xlsx") 
#     if len(errors) == 0:
#         print("Everything seems ok.")
#     else:
#         for err in errors: print(err)
