from . import amea_thess, epas, pepas, amea_ath, saek

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
        saek.migrate_excel(filepath)
        return errors
    elif id == 33:
        print("migrating amea thess")
        amea_thess.migrate_excel(filepath)
        return errors
    elif id == 95:
        print("migrating amea ath")
        amea_ath.migrate_excel(filepath)
        return errors
    return []