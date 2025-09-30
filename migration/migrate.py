from . import epas

def migrate_school(id, filepath):
    print("migrate_school id:", id, "filepath: ", filepath)
    if str(id) == '1':
        print("migrating epas")
        errors = []
        epas.migrate_excel(filepath)
        return errors
    return []