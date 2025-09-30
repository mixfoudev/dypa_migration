import pandas as pd
import re
from app.service import static_data_service as staticService
from app.service import epas_service

# expected columns
COLUMNS = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΕΙΔΙΚΟΤΗΤΑ", "ΤΑΞΗ", "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ","ΑΔΤ",
    "ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ", "ΑΡ. ΔΗΜΟΤΟΛΟΓ", "ΧΩΡΑ", "IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ", "ΑΜ",
    "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
    #,"ΑΔΙΚ.ΑΠΟΥΣΙΕΣ","ΜΗ ΜΕΤΡ.ΑΠΟΥΣΙΕΣ","ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ","ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ"
    ,"ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ","ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ"
]

def section_from_row(row):
    d ={}
    d['section'] = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']
    d['acYear'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ']
    d['period'] = row['ΤΑΞΗ']
    d['grade'] = float(row['ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ'])
    d['studyNum'] = row['ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ']
    return d

def contact_from_row(row):
    d ={}
    d['email'] = row['EMAIL']
    d['mobile'] = row['ΚΙΝΗΤΟ ΤΗΛ']
    d['phone'] = row['ΣΤΑΘΕΡΟ ΤΗΛ']
    d['address'] = row['ΔΙΕΥΘΥΝΣΗ']
    d['addressNum'] = row['ΑΡΙΘΜΟΣ']
    d['city'] = row['ΠΟΛΗ']
    d['zipcode'] = row['ΤΚ']
    return d

def user_from_row(row):
    d ={}
    d['vat'] = row['ΑΦΜ']
    d['lastname'] = row['ΕΠΩΝΥΜΟ']
    d['name'] = row['ΟΝΟΜΑ']
    d['flastname'] = row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ']
    d['fname'] = row['ΟΝΟΜΑ ΠΑΤΕΡΑ']
    d['mlastname'] = row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ']
    d['mname'] = row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ']
    d['dob'] = row['ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ']
    d['gender'] = row['ΦΥΛΟ']
    return d

def personal_from_row(row):
    d ={}
    d['amka'] = row['ΑΜΚΑ']
    d['ama'] = row['ΑΜΑ']
    d['identity'] = row['ΑΔΤ']
    d['munRegister'] = row['ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ']
    d['cencusNum'] = row['ΑΡ. ΔΗΜΟΤΟΛΟΓ']
    d['country'] = row['ΧΩΡΑ']
    d['iban'] = row['IBAN']
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ']
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α']
    d['birthPlace'] = row['ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ']
    return d

def student_from_row(row):
    d ={}
    d['kpa'] = row['ΚΠΑ']
    d['noSkipLessons'] = row['ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ']
    d['am'] = row['ΑΜ']
    d['dateRegister'] = row['ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ']
    d['acYearRegister'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ']
    d['edu'] = row['ΣΧΟΛΗ']
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ']
    return d

def row_to_dto(row):
    d ={}
    d['section'] = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ']
    d['acYear'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ']
    d['period'] = row['ΤΑΞΗ']
    d['vat'] = row['ΑΦΜ']
    d['lastname'] = row['ΕΠΩΝΥΜΟ']
    d['name'] = row['ΟΝΟΜΑ']
    d['flastname'] = row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ']
    d['fname'] = row['ΟΝΟΜΑ ΠΑΤΕΡΑ']
    d['mlastname'] = row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ']
    d['mname'] = row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ']
    d['dob'] = row['ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ']
    d['gender'] = row['ΦΥΛΟ']
    d['email'] = row['EMAIL']
    d['mobile'] = row['ΚΙΝΗΤΟ ΤΗΛ']
    d['phone'] = row['ΣΤΑΘΕΡΟ ΤΗΛ']
    d['address'] = row['ΔΙΕΥΘΥΝΣΗ']
    d['addressNum'] = row['ΑΡΙΘΜΟΣ']
    d['city'] = row['ΠΟΛΗ']
    d['zipcode'] = row['ΤΚ']#20
    d['amka'] = row['ΑΜΚΑ']
    d['ama'] = row['ΑΜΑ']
    d['birthPlace'] = row['ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ']
    d['munRegister'] = row['ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ']
    d['cencusNum'] = row['ΑΡ. ΔΗΜΟΤΟΛΟΓ']
    d['country'] = row['ΧΩΡΑ']
    d['iban'] = row['IBAN']
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ']
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α']
    d['kpa'] = row['ΚΠΑ']
    d['noSkipLessons'] = row['ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ']
    d['am'] = row['ΑΜ']
    d['dateRegister'] = row['ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ']
    d['acYearRegister'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ']
    d['edu'] = row['ΣΧΟΛΗ']
    d['grade'] = row['ΒΑΘΜΟΣ ΠΡΟΗΓ. ΤΑΞΗΣ']
    d['studyNum'] = row['ΑΡΙΘ. ΦΟΙΤΗΣΕΩΝ']
    return d

def calc_period(tp):
    if not tp: return None
    if tp.upper() in ["Α", "Α'", "Α ΤΆΞΗ", "Α ΤΑΞΗ"]: return 1
    if tp.upper() in ["Β", "Β'", "Β ΤΆΞΗ", "Β ΤΑΞΗ"]: return 2
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

    elif field_name == "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ":
        return value and value in ['ΝΑΙ', 'ΟΧΙ']

    # epas specific
    elif field_name == "ΤΑΞΗ":
        return value and calc_period(value) in [1,2]
    
    elif field_name == "ΣΧΟΛΗ":
        return value and staticService.edu_exists(1, value)
    
    elif field_name == "ΧΩΡΑ":
        return value and staticService.country_exists(value)

    return True

def migrate_excel(file_path):
    df = pd.read_excel(file_path, dtype=str)
    dtos = []
    for i, row in df.iterrows():
        dto = row_to_dto(row)
        classStud = section_from_row(row)
        contact = contact_from_row(row)
        personal = personal_from_row(row)
        student = student_from_row(row)
        user = user_from_row(row)
        dtos.append(dto)
        print("saving row")
        epas_service.save(user, contact, personal, student, classStud)
    
