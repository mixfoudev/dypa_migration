import pandas as pd
import re
from app.service import static_data_service as staticService
from validation import general_validations as v
from app import util as u

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
prev_periods = {}
prev_years = []
unique_vats = []
unique_adts = []
existing_students=[]
unique_ams = {}
students = {"total": 0, "data": []}
section_students = {}
part_students = {}
acPeriods = {}

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

def validate_ac_year(value):
    try:
        start, end = value.split("/")
        if len(start) != 4 or len(end) != 4: return False
        if int(start) >= int(end) : return False
        if not (int(start) +1) == int(end) : return False
        return True
    except:
        return False

def _needsPrevYear(periodNum, row):
    if periodNum in [1,3] and (pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ'])): return True
    if periodNum in [2,4] and (pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])): return True
    return False

def validate_prev_lesson_fields(row, err):
    for i, field in enumerate(pending_cols):
        # if i == 3:
        #     if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']) and ( pd.notna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']) or pd.notna(row['ΕΞΑΜΗΝΟ']) ):
        #         err.append(field)
        #         continue
        value = row[field]
        valid = pd.isna(value) or (v.isNumber(value, int) and staticService.lesson_exists(row['ΕΙΔΙΚΟΤΗΤΑ'], i + 1 , value))
        if not valid: err.append(field)

def check_prev_years(row, period, err):
    if period and 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ' not in err and _needsPrevYear(period, row):
        tp = {1:"Α ΕΞΑΜ",2:"Β ΕΞΑΜ",3:"Γ ΕΞΑΜ",4:"Δ ΕΞΑΜ"}
        acYearL = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].split("/")
        prevStr = f"{int(acYearL[0])-1}/{int(acYearL[1])-1}"
        if prevStr not in prev_years: prev_years.append(prevStr)
        
        prevYear = staticService.get_ac_year(prevStr)
        if prevStr not in acPeriods.keys(): 
            periods = [p for p in prevYear['periods'] if int(p['dypa_inst_type_id']) == 3]
            acPeriods[prevStr] = [int(p['num']) for p in periods] if len(periods) > 0 else []
        
        if any([s in err for s in pending_cols]): return
        periodNums = acPeriods[prevStr]
        if period in [1,3] and (pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ'])): 
            if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']) and 1 not in periodNums:
                if prevStr not in prev_periods.keys(): prev_periods[prevStr]=[]
                if tp[1] not in prev_periods[prevStr]: prev_periods[prevStr].append(tp[1])
            elif pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ']) and 3 not in periodNums:
                if prevStr not in prev_periods.keys(): prev_periods[prevStr]=[]
                if tp[3] not in prev_periods[prevStr]: prev_periods[prevStr].append(tp[3])
        if period in [2,4] and (pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']) or pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])): 
            if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']) and tp[2] not in periodNums:
                if prevStr not in prev_periods.keys(): prev_periods[prevStr]=[]
                if tp[2] not in prev_periods[prevStr]: prev_periods[prevStr].append(tp[2])
            elif pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']) and 4 not in periodNums:
                if prevStr not in prev_periods.keys(): prev_periods[prevStr]=[]
                if tp[4] not in prev_periods[prevStr]: prev_periods[prevStr].append(tp[4])
        #


def validate_personal(row):
    col = ["ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ","ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ", "ΑΔΤ", "ΧΩΡΑ", 
    #,"ΑΜ ΑΡΡΕΝΩΝ","ΑΡ. ΔΗΜΟΤΟΛΟΓ","ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ","ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ","ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ",  "IBAN", "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ"
    ]
    return v.validate_personal(row, col, students, existing_students, unique_vats, unique_adts)

def validate_student(row, prevErr):
    col = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ","ΕΞΑΜΗΝΟ", 
    "ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ"
    ]
    err = []
    period = None
    spec = None
    sxoli = None
    sec = None

    onlyPart = (pd.isna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']) and pd.isna(row['ΕΞΑΜΗΝΟ'])) and pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])
    print("onlyPart: ", onlyPart)

    if not 'ΕΙΔΙΚΟΤΗΤΑ' in prevErr: validate_prev_lesson_fields(row, err)

    if onlyPart: 
        period = 4
        check_prev_years(row, period, prevErr)
    else:# not only part
        if pd.isna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']): err.append("ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ")
        if pd.isna(row['ΕΞΑΜΗΝΟ']): err.append("ΕΞΑΜΗΝΟ")
        else:
            value = row['ΕΞΑΜΗΝΟ']
            period = calc_period(value)
            if period is None or period not in [1,2,3,4]: err.append("ΕΞΑΜΗΝΟ")

        if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']): err.append("Δεν μπορεί να υπάρχει ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ σε πλήρη φοίτηση")    

        if period:
            pendValError = validate_pending_lesson(row, period)
            if pendValError: err.append(pendValError)
            else: check_prev_years(row, period, prevErr)

        allErr = err + prevErr
        sec_val = ['ΣΧΟΛΗ', 'ΕΞΑΜΗΝΟ', 'ΕΙΔΙΚΟΤΗΤΑ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ', 'ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']
        if all([s not in allErr for s in sec_val]):
            sec = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ'].strip()
            spec = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
            sxoli = row['ΣΧΟΛΗ'].strip()
            valid = staticService.class_section_exists(dypaId, sec, row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'], period, spec, sxoli)
            print("section is valid: ", valid)
            if not valid:
                allErr.append("ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ")
                err.append("ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ")
       
    if len(err) == 0:
        vat = row['ΑΦΜ'].strip()
        if onlyPart:
            if not 'data' in part_students.keys(): part_students['data'] = []
            if not vat in part_students['data']: part_students['data'].append(vat)
        else:
            if sec:
                if not sec in section_students.keys(): section_students[sec] = {"name":sec,"total": 0, "exist": False, "data": []}
                if not vat in section_students[sec]['data']: section_students[sec]['data'].append(vat)
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
  
    prev_p = {}
    for p in prev_periods.keys():
        if len(prev_periods[p]) > 0: prev_p[p]=prev_periods[p]

    data = {"errors": errors,"section_students": section_students,"students": students if len(students['data']) > 0 else None, "part_students": part_students}
    acYears = check_academic_years(df)
    data['ac_years'] = sorted(acYears, key=lambda x: x['name'])
    data['prev_periods'] = prev_p
    print("acYears: ", acYears)
    data['existing_students'] = existing_students
    return data
