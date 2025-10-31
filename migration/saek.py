import pandas as pd
import re
from app.service import static_data_service as staticService
from app.service import saek_service

# expected columns
COLUMNS = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΕΙΔΙΚΟΤΗΤΑ", "ΕΞΑΜΗΝΟ", "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ","ΑΔΤ",
    "ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ", "ΑΡ. ΔΗΜΟΤΟΛΟΓ", "ΧΩΡΑ", "IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΑΜ",
    "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
    ,"ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ","ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ"
]

def section_from_row(row):
    onlyPart = pd.isna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']) and pd.isna(row['ΕΞΑΜΗΝΟ']) and pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])
    d ={}
    d['section'] = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ'].strip() if not onlyPart else None
    d['acYear'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].strip()
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
    d['period'] = row['ΕΞΑΜΗΝΟ'].strip() if not onlyPart else 'Δ'
    d['periodNum'] = int(calc_period(d['period']))
    d['grade'] = None
    d['studyNum'] = None #row['ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ'].strip()
    return d

def contact_from_row(row):
    d ={}
    d['email'] = row['EMAIL'].strip()
    d['mobile'] = row['ΚΙΝΗΤΟ ΤΗΛ'].strip()
    d['phone'] = row['ΣΤΑΘΕΡΟ ΤΗΛ'].strip()
    d['address'] = row['ΔΙΕΥΘΥΝΣΗ'].strip()
    d['addressNum'] = row['ΑΡΙΘΜΟΣ'].strip()
    d['city'] = row['ΠΟΛΗ'].strip()
    d['zipcode'] = row['ΤΚ'].strip()
    return d

def user_from_row(row):
    d ={}
    d['vat'] = row['ΑΦΜ'].strip()
    d['lastname'] = row['ΕΠΩΝΥΜΟ'].strip()
    d['name'] = row['ΟΝΟΜΑ'].strip()
    d['fname'] = row['ΟΝΟΜΑ ΠΑΤΕΡΑ'].strip()
    d['flastname'] = row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ'].strip() if pd.notna(row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ']) else None
    d['mlastname'] = row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ'].strip() if pd.notna(row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ']) else None
    d['mname'] = row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ'].strip() if pd.notna(row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ']) else None
    d['dob'] = row['ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ'].strip()
    d['gender'] = row['ΦΥΛΟ'].strip()
    return d

def personal_from_row(row):
    d ={}
    d['amka'] = row['ΑΜΚΑ'].strip()
    d['ama'] = row['ΑΜΑ'].strip() if pd.notna(row['ΑΜΑ']) else None
    d['iban'] = row['IBAN'].strip() if pd.notna(row['IBAN']) else None
    d['identity'] = row['ΑΔΤ'].strip()
    d['munRegister'] = row['ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ'].strip()
    d['cencusNum'] = row['ΑΡ. ΔΗΜΟΤΟΛΟΓ'].strip()
    d['country'] = row['ΧΩΡΑ'].strip()
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ'].strip() if pd.notna(row['ΑΜ ΑΡΡΕΝΩΝ']) else None
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α'].strip() if pd.notna(row['ΤΟΠ ΕΓΓ Μ.Α']) else None
    d['birthPlace'] = row['ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ'].strip()
    return d

def student_from_row(row):
    d ={}
    d['kpa'] = row['ΚΠΑ'].strip() if pd.notna(row['ΚΠΑ']) else None
    d['attendGeneralLesson'] = None
    d['am'] = row['ΑΜ'].strip()
    d['dateRegister'] = row['ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ'].strip()
    d['acYearRegister'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].strip()
    d['edu'] = row['ΣΧΟΛΗ'].strip()
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
    d['pendLes1'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']) else None
    d['pendLes2'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']) else None
    d['pendLes3'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ']) else None
    d['pendLes4'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']) else None
    return d

def row_to_dto(row):
    onlyPart = pd.isna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']) and pd.isna(row['ΕΞΑΜΗΝΟ']) and pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])
    d ={}
    d['section'] = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ'].strip() if not onlyPart else None
    d['acYear'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].strip()
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
    d['period'] = row['ΕΞΑΜΗΝΟ'].strip() if not onlyPart else 'Δ'
    d['vat'] = row['ΑΦΜ'].strip()
    d['lastname'] = row['ΕΠΩΝΥΜΟ'].strip()
    d['name'] = row['ΟΝΟΜΑ'].strip()
    d['fname'] = row['ΟΝΟΜΑ ΠΑΤΕΡΑ'].strip()
    d['flastname'] = row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ'].strip() if pd.notna(row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ']) else None
    d['mlastname'] = row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ'].strip() if pd.notna(row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ']) else None
    d['mname'] = row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ'].strip() if pd.notna(row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ']) else None
    d['dob'] = row['ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ'].strip()
    d['gender'] = row['ΦΥΛΟ'].strip()
    d['email'] = row['EMAIL'].strip()
    d['mobile'] = row['ΚΙΝΗΤΟ ΤΗΛ'].strip()
    d['phone'] = row['ΣΤΑΘΕΡΟ ΤΗΛ'].strip()
    d['address'] = row['ΔΙΕΥΘΥΝΣΗ'].strip()
    d['addressNum'] = row['ΑΡΙΘΜΟΣ'].strip()
    d['city'] = row['ΠΟΛΗ'].strip()
    d['zipcode'] = row['ΤΚ'].strip()#20
    d['amka'] = row['ΑΜΚΑ'].strip()
    d['ama'] = row['ΑΜΑ'].strip() if pd.notna(row['ΑΜΑ']) else None
    d['iban'] = row['IBAN'].strip() if pd.notna(row['IBAN']) else None
    d['birthPlace'] = row['ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ'].strip()
    d['munRegister'] = row['ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ'].strip()
    d['cencusNum'] = row['ΑΡ. ΔΗΜΟΤΟΛΟΓ'].strip()
    d['country'] = row['ΧΩΡΑ'].strip()
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ'].strip() if pd.notna(row['ΑΜ ΑΡΡΕΝΩΝ']) else None
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α'].strip() if pd.notna(row['ΤΟΠ ΕΓΓ Μ.Α']) else None
    d['kpa'] = row['ΚΠΑ'].strip() if pd.notna(row['ΚΠΑ']) else None
    d['attendGeneralLesson'] = None
    d['am'] = row['ΑΜ'].strip()
    d['dateRegister'] = row['ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ'].strip()
    d['acYearRegister'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].strip()
    d['edu'] = row['ΣΧΟΛΗ'].strip()
    d['grade'] = None
    d['studyNum'] = None #row['ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ'].strip()
    d['pendLes1'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Α ΕΞΑΜ']) else None
    d['pendLes2'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Β ΕΞΑΜ']) else None
    d['pendLes3'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Γ ΕΞΑΜ']) else None
    d['pendLes4'] = int(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'].strip()) if pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ']) else None
    return d

def calc_period(tp):
    if not tp: return None
    if tp.upper() in ["Α", "Α'", "Α ΕΞΑΜΗΝΟ", "Α ΕΞΆΜΗΝΟ"]: return 1
    if tp.upper() in ["Β", "Β'", "Β ΕΞΑΜΗΝΟ", "Β ΕΞΆΜΗΝΟ"]: return 2
    if tp.upper() in ["Γ", "Γ'", "Γ ΕΞΑΜΗΝΟ", "Γ ΕΞΆΜΗΝΟ"]: return 3
    if tp.upper() in ["Δ", "Δ'", "Δ ΕΞΑΜΗΝΟ", "Δ ΕΞΆΜΗΝΟ"]: return 4
    return None

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

def validate_field(field_name, value):
    if field_name == "ΑΜ":
        try:
            int(value)
            return True
        except Exception as e:
            return False

    if field_name == "ΑΦΜ":
        return isinstance(value, (int, float, str)) and str(value).isdigit() and len(str(value)) == 9

    if field_name == "ΑΜ":
        return isinstance(value, (int, float, str)) and str(value).isdigit() and len(str(value)) >0

    elif field_name == "EMAIL":
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, str(value)))

    elif field_name in ["ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ"]:
        return is_valid_date(value)

    elif field_name == "ΦΥΛΟ":
        return str(value).strip().lower() in ["α", "θ"]

    elif field_name == "ΤΚ":
        return str(value).isdigit() and len(str(value)) == 5
    
    elif field_name == "ΕΙΔΙΚΟΤΗΤΑ":
        return staticService.spec_exists(1, value)
    
    elif field_name in ["ΑΚΑΔ. ΕΤΟΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ"]:
        try:
            start, end = value.split("/")
            if len(start) != 4 or len(end) != 4: return False
            if int(start) >= int(end) : return False
            if not (int(start) +1) == int(end) : return False
            return True
        except Exception as e:
            return False

    # epas specific
    elif field_name == "ΕΞΑΜΗΝΟ":
        return pd.notna(value) and calc_period(value) in [1,2,3,4]
    
    elif field_name == "ΣΧΟΛΗ":
        return value and staticService.edu_exists(1, value)
    
    elif field_name == "ΧΩΡΑ":
        return value and staticService.country_exists(value)

    return True

def migrate_excel(file_path):
    df = pd.read_excel(file_path, dtype=str)
    
    dtos = []
    for i, row in df.iterrows():
        onlyPart = pd.isna(row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']) and pd.isna(row['ΕΞΑΜΗΝΟ']) and pd.notna(row['ΧΡΩΣΤΟΥΜ. ΜΑΘ. Δ ΕΞΑΜ'])
        dto = row_to_dto(row)
        classStud = section_from_row(row)
        contact = contact_from_row(row)
        personal = personal_from_row(row)
        student = student_from_row(row)
        user = user_from_row(row)
        dtos.append(dto)
        student['onlyPart'] = onlyPart
        print("saving row")
        saek_service.save(user, contact, personal, student, classStud)
    
