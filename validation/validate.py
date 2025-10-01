from . import epas

def validate_school(id, filepath):
    print("validate_school id:", id, "filepath: ", filepath)
    if id == 1:
        print("validating epas")
        errors = epas.validate_excel(filepath)
        #print("erorrs: ", errors)
        return errors
    elif id == 2:
        print("validating pepas")
        #epas.validate_excel(filepath)
        return errors
    elif id == 3:
        print("validating saek")
        #epas.validate_excel(filepath)
        return errors
    elif id == 33:
        print("validating amea thess")
        #epas.validate_excel(filepath)
        return errors
    elif id == 95:
        print("validating amea ath")
        #epas.validate_excel(filepath)
        return errors
    return []