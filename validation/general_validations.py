import pandas as pd
import re
from app.service import static_data_service as staticService


def check_academic_years(df, dypaId):
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

def eduSpecMissing(row, err):
    for s in ['ΕΙΔΙΚΟΤΗΤΑ', 'ΣΧΟΛΗ', 'ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ']: 
        if s in err: True
    eduSpecId = staticService.get_edu_year_spec(row['ΣΧΟΛΗ'].strip(), row['ΑΚΑΔ. ΕΤΟΣ ΕΙΣΑΓΩΓΗΣ'], row['ΕΙΔΙΚΟΤΗΤΑ'].strip())
    return eduSpecId is None

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
    
def validate_personal(row, col, students, existing_students, unique_vats, unique_adts):
    err = []
    for field_name in col:
        if field_name not in row: continue
        value = row[field_name]
        #print(f"p val field: {field_name} | value: {value} | isna: {pd.isna(value)}")
        if pd.isna(value): 
            err.append(field_name)
            continue
        valid = True
        if field_name == "ΑΔΤ":
            valid = len(str(value)) > 5

        elif field_name == "ΑΦΜ":
            valid = isinstance(value, (int, float, str)) and str(value).isdigit() and len(str(value)) == 9

        elif field_name == "ΚΙΝΗΤΟ ΤΗΛ":
            valid =  str(value).isdigit() and len(str(value)) >= 10
        
        elif field_name == "EMAIL":
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            valid = bool(re.match(pattern, str(value)))

        elif field_name in ["ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ"]:
            valid = is_valid_date(value)

        elif field_name == "ΦΥΛΟ":
            valid = str(value).strip().lower() in ["α", "θ"]

        elif field_name == "ΤΚ":
            valid = str(value).isdigit() and len(str(value)) == 5
        
        elif field_name == "ΧΩΡΑ":
            valid = staticService.country_exists(value)

        if not valid: err.append(field_name)

    if "ΑΦΜ" not in err:
        vat = row['ΑΦΜ']
        if vat not in unique_vats:
            unique_vats.append(vat)
            if staticService.student_exists_by_vat(vat):
                existing_students.append(vat)
        else: err.append("Διπλότυπος ΑΦΜ")
    if "ΑΔΤ" not in err:
        adt = row['ΑΔΤ']
        if adt not in unique_adts:
            unique_adts.append(adt)
        else: err.append("Διπλότυπος ΑΔΤ")
    
    if len(err) == 0:
        students["data"].append({"vat":row['ΑΦΜ'], "lastname":row['ΕΠΩΝΥΜΟ'], "name":row['ΟΝΟΜΑ']})
    return err
