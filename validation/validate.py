from . import epas, pepas, amea_ath, amea_thess

def validate_school(id, filepath):
    print("validate_school id:", id, "filepath: ", filepath)
    errors = {}
    if id == 1:
        print("validating epas")
        errors = epas.validate_excel(filepath)
        #print("erorrs: ", errors)
        return errors
    elif id == 2:
        print("validating pepas")
        errors = pepas.validate_excel(filepath)
        return errors
    elif id == 3:
        print("validating saek")
        #errors = epas.validate_excel(filepath)
        return errors
    elif id == 33:
        print("validating amea thess")
        errors = amea_thess.validate_excel(filepath)
        return errors
    elif id == 95:
        print("validating amea ath")
        errors = amea_ath.validate_excel(filepath)
        return errors
    return []