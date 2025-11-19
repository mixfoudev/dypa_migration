import pandas as pd
from app.service import amea_ath_service
from app import util as u

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
    d['period_num'] = int(row['ΕΤΟΣ'].strip())
    d['grade'] = float(row['ΒΑΘΜΟΣ Μ.Ο'].strip()) if d['period'] == 2 else None
    d['abs'] = int(row['ΑΔΙΚ.ΑΠΟΥΣΙΕΣ'].strip()) if d['period'] == 2 else None
    d['justAbs'] = int(row['ΔΙΚΑΙΟΛ. ΑΠΟΥΣΙΕΣ'].strip()) if d['period'] == 2 else None
    return d

def contact_from_row(row):
    d ={}
    d['email'] = row['EMAIL'].strip()
    d['mobile'] = row['ΚΙΝΗΤΟ ΤΗΛ'].strip() if pd.notna(row['ΚΙΝΗΤΟ ΤΗΛ']) else None
    d['phone'] = row['ΣΤΑΘΕΡΟ ΤΗΛ'].strip() if pd.notna(row['ΣΤΑΘΕΡΟ ΤΗΛ']) else None
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
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ'].strip() if pd.notna(row['ΑΜ ΑΡΡΕΝΩΝ']) else None
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α'].strip() if pd.notna(row['ΤΟΠ ΕΓΓ Μ.Α']) else None
    d['citizenship'] = row['ΥΠΗΚΟΟΤΗΤΑ'].strip() if pd.notna(row['ΥΠΗΚΟΟΤΗΤΑ']) else None
    return d

def student_from_row(row):
    d ={}
    d['kpa'] = row['ΚΠΑ'].strip() if pd.notna(row['ΚΠΑ']) else None
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
    #d['period'] = int(row['ΕΤΟΣ'].strip())
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
    d['mobile'] = row['ΚΙΝΗΤΟ ΤΗΛ'].strip() if pd.notna(row['ΚΙΝΗΤΟ ΤΗΛ']) else None
    d['phone'] = row['ΣΤΑΘΕΡΟ ΤΗΛ'].strip() if pd.notna(row['ΣΤΑΘΕΡΟ ΤΗΛ']) else None
    d['address'] = row['ΔΙΕΥΘΥΝΣΗ'].strip()
    d['addressNum'] = row['ΑΡΙΘΜΟΣ'].strip()
    d['city'] = row['ΠΟΛΗ'].strip()
    d['zipcode'] = row['ΤΚ'].strip()#20
    d['amka'] = row['ΑΜΚΑ'].strip()
    d['ama'] = row['ΑΜΑ'].strip() if pd.notna(row['ΑΜΑ']) else None
    d['iban'] = row['IBAN'].strip() if pd.notna(row['IBAN']) else None
    d['maleRegId'] = row['ΑΜ ΑΡΡΕΝΩΝ'].strip() if pd.notna(row['ΑΜ ΑΡΡΕΝΩΝ']) else None
    d['makeRegPlace'] = row['ΤΟΠ ΕΓΓ Μ.Α'].strip() if pd.notna(row['ΤΟΠ ΕΓΓ Μ.Α']) else None
    d['kpa'] = row['ΚΠΑ'].strip() if pd.notna(row['ΚΠΑ']) else None
    d['am'] = row['ΑΜ'].strip()
    d['dateRegister'] = row['ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ'].strip()
    d['acYearRegister'] = row['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].strip()
    d['edu'] = row['ΣΧΟΛΗ'].strip()
    # d['grade'] = row['ΒΑΘΜΟΣ Μ.Ο'].strip()
    # d['abs'] = int(row['ΑΔΙΚ.ΑΠΟΥΣΙΕΣ'].strip())
    # d['justAbs'] = int(row['ΔΙΚΑΙΟΛ. ΑΠΟΥΣΙΕΣ'].strip())
    d['kepa'] = row['ΠΑΘΗΣΗ ΚΕΠΑ'].strip()
    return d

def migrate_excel(file_path):
    # df = pd.read_excel(file_path, dtype=str)
    df = u.load_excel(file_path)
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
    
