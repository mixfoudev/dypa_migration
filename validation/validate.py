from . import epas

def validate_school(id, filepath):
    print("validate_school id:", id, "filepath: ", filepath)
    if id == '1':
        print("validating epas")
        errors = epas.validate_excel(filepath)
        #print("erorrs: ", errors)
        return errors
    return []