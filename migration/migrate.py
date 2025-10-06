from . import epas, pepas

def migrate_school(id, filepath):
    print("migrate_school id:", id, "filepath: ", filepath)
    errors = []
    if id == 1:
        print("migrating epas")
        epas.migrate_excel(filepath)
        return errors
    elif id == 2:
        print("migrating pepas")
        pepas.migrate_excel(filepath)
        return errors
    elif id == 3:
        print("migrating saek")
        #epas.migrate_excel(filepath)
        return errors
    elif id == 33:
        print("migrating amea thess")
        #epas.migrate_excel(filepath)
        return errors
    elif id == 95:
        print("migrating amea ath")
        #epas.migrate_excel(filepath)
        return errors
    return []