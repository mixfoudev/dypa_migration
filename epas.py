from ast import List
import pandas as pd
from validation import validate

# expected columns
COLUMNS = [
    "ΤΜΗΜΑ", "ΑΚΑΔ. ΕΤΟΣ", "ΕΙΔΙΚΟΤΗΤΑ", "ΤΑΞΗ", "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ",
    "ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ", "ΑΡ. ΔΗΜΟΤΟΛΟΓ", "ΧΩΡΑ", "IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ", "ΑΜ",
    "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
]

def check_academic_years(df):
    ac = df['ΑΚΑΔ. ΕΤΟΣ'].unique().tolist()
    reg = df['ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ'].unique().tolist()
    ac_years = list(set(ac + reg))
    print(ac)
    print(reg)
    print(ac_years)

if __name__ == "__main__":
    #errors = validate.validate_school(1, "data/epas.xlsx")
    df = pd.read_excel("data/epas.xlsx", dtype=str)
    check_academic_years(df)
    
    
