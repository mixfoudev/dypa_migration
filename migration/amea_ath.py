import pandas as pd
from app.service import amea_ath_service

# expected columns
COLUMNS = [
    "ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ", "ΕΤΟΣ", "ΠΑΘΗΣΗ ΚΕΠΑ", "ΕΙΔΙΚΟΤΗΤΑ",  "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ", "ΥΠΗΚΟΟΤΗΤΑ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ","ΑΔΤ","IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΑΜ","ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
    ,"ΑΔΙΚ.ΑΠΟΥΣΙΕΣ","ΔΙΚΑΙΟΛ. ΑΠΟΥΣΙΕΣ","ΒΑΘΜΟΣ Μ.Ο"
]

def section_from_row(row):
    d ={}
    d['section'] = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ'].strip()
    d['acYear'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].strip()
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
    d['period'] = int(row['ΕΤΟΣ'].strip())
    d['grade'] = float(row['ΒΑΘΜΟΣ Μ.Ο'].strip())
    d['abs'] = int(row['ΑΔΙΚ.ΑΠΟΥΣΙΕΣ'].strip())
    d['justAbs'] = int(row['ΔΙΚΑΙΟΛ. ΑΠΟΥΣΙΕΣ'].strip())
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
    d['flastname'] = row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ'].strip()
    d['fname'] = row['ΟΝΟΜΑ ΠΑΤΕΡΑ'].strip()
    d['mlastname'] = row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ'].strip()
    d['mname'] = row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ'].strip()
    d['dob'] = row['ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ'].strip()
    d['gender'] = row['ΦΥΛΟ'].strip()
    return d

def personal_from_row(row):
    d ={}
    d['amka'] = row['ΑΜΚΑ'].strip()
    d['ama'] = row['ΑΜΑ'].strip()
    d['identity'] = row['ΑΔΤ'].strip()
    d['iban'] = row['IBAN'].strip()
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ'].strip()
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α'].strip()
    d['citizenship'] = row['ΥΠΗΚΟΟΤΗΤΑ'].strip()
    return d

def student_from_row(row):
    d ={}
    d['kpa'] = row['ΚΠΑ'].strip()
    d['am'] = row['ΑΜ'].strip()
    d['dateRegister'] = row['ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ'].strip()
    d['acYearRegister'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].strip()
    d['edu'] = row['ΣΧΟΛΗ'].strip()
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
    d['kepa'] = row['ΠΑΘΗΣΗ ΚΕΠΑ'].strip()
    return d

def row_to_dto(row):
    d ={}
    d['section'] = row['ΤΜΗΜΑ ΕΙΣΑΓΩΓΗΣ'].strip()
    d['acYear'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'].strip()
    d['spec'] = row['ΕΙΔΙΚΟΤΗΤΑ'].strip()
    d['period'] = int(row['ΕΤΟΣ'].strip())
    d['vat'] = row['ΑΦΜ'].strip()
    d['lastname'] = row['ΕΠΩΝΥΜΟ'].strip()
    d['name'] = row['ΟΝΟΜΑ'].strip()
    d['flastname'] = row['ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ'].strip()
    d['fname'] = row['ΟΝΟΜΑ ΠΑΤΕΡΑ'].strip()
    d['mlastname'] = row['ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ'].strip()
    d['mname'] = row['ΟΝΟΜΑ ΜΗΤΕΡΑΣ'].strip()
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
    d['ama'] = row['ΑΜΑ'].strip()
    d['iban'] = row['IBAN'].strip()
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ'].strip()
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α'].strip()
    d['kpa'] = row['ΚΠΑ'].strip()
    d['am'] = row['ΑΜ'].strip()
    d['dateRegister'] = row['ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ'].strip()
    d['acYearRegister'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].strip()
    d['edu'] = row['ΣΧΟΛΗ'].strip()
    d['grade'] = row['ΒΑΘΜΟΣ Μ.Ο'].strip()
    d['abs'] = int(row['ΑΔΙΚ.ΑΠΟΥΣΙΕΣ'].strip())
    d['justAbs'] = int(row['ΔΙΚΑΙΟΛ. ΑΠΟΥΣΙΕΣ'].strip())
    d['kepa'] = row['ΠΑΘΗΣΗ ΚΕΠΑ'].strip()
    return d

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
        amea_ath_service.save(user, contact, personal, student, classStud)
    
