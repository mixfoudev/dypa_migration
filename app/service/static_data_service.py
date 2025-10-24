from app.db import queries as q

hash_specs = {}
hash_sections = {}
hash_years = {}
hash_edu = {}
ac_years = []
countries = []
edu_year_specs = {}
edu_ids = {}
edu_ams = {}
spec_ids = {}
class_lessons = {}
class_lessonsEpas = {}

def student_exists_by_vat(vat):
    c = len(q.active_student_exists_by_vat(vat))
    #print("active students: ", c)
    return c > 0

def get_edu_year_spec(edu, acName, specName):
    acYear = get_ac_year(acName)
    eduId = get_edu_id(edu)
    if not acYear or not eduId: return None
    if not specName in spec_ids.keys(): return None
    acId = acYear['id']
    specId = spec_ids[specName]
    key = f"{eduId}_{acId}_{specId}"
    if key not in edu_year_specs.keys():
        edu_year_specs[key] = q.get_edu_year_spec(eduId, acId, specId)
    return edu_year_specs[key]

def spec_exists(dypaId, name):
    if not dypaId in hash_specs.keys():
        specs = q.get_student_specs(dypaId)
        hash_specs[dypaId] = specs
        for s in specs:
            spec_ids[s['name']] = s['id']
    return name in [s['name'] for s in hash_specs[dypaId]]

def get_class_section_id(dypaId, name):
    sections = [x for x in hash_sections[dypaId] if x['title'] == name]
    if len(sections) == 0: return None
    return sections[0]

def get_class_lessons(classId):
    if not classId in class_lessons.keys():
        lessons = q.get_class_lessons(classId)
        class_lessons[classId] = lessons
    return class_lessons[classId]

def get_class_lessonsEpas(classId):
    if not classId in class_lessonsEpas.keys():
        lessons = q.get_class_lessonsWithEpasLessonType(classId)
        class_lessonsEpas[classId] = lessons
    return class_lessonsEpas[classId]

def class_section_exists(dypaId, name, acName):
    if not dypaId in hash_sections.keys():
        hash_sections[dypaId] = q.get_class_sections(dypaId)
    #print("aaaaaaaaaaa:   ", hash_sections[dypaId])
    return name in [s['title'] for s in hash_sections[dypaId] if s['acName'] == acName]

def edu_exists(dypaId, name):
    if not dypaId in hash_edu.keys():
        dypaSchools = q.get_schools(dypaId)
        hash_edu[dypaId] = dypaSchools
        for e in dypaSchools:
            edu_ids[e['name']]=e['id']
            amRes = q.get_ams_for_edu(e['id'])
            #print("amRes:", amRes)
            edu_ams[e['id']] = [s['am'] for s in amRes]
            #print("edu_ams" ,edu_ams[e['id']])
    #print("aaaa hashedu:", hash_edu)
    #print(f"name: '{name}'")
    return name in [s['name'] for s in hash_edu[dypaId]]

def get_edu_ams(dypaId, name):
    if not edu_exists(dypaId, name): return []
    out = edu_ams[edu_ids[name]]
    #print("get_edu_ams: ", out)
    return out

def get_countries():
    global countries
    if len(countries) == 0:
        countries = q.get_countries()
    return countries

def get_country_id(country):
    if not country: return None
    c = [s for s in get_countries() if s['name'] == country]
    if len(c) == 0: return None
    return c[0]['id']


def country_exists(name):
    data = get_countries()
    #print("counties: ", data)
    return name in [c['name'] for c in data]

def get_academic_years(refresh=False):
    global ac_years
    if len(ac_years) == 0 or refresh:
        ac_years = q.get_academic_years()
        for ac in ac_years:
            ac['periods'] = q.get_academic_year_periods(ac['id'])
    return ac_years

def get_ac_year(name):
    if not name in hash_years.keys():
        l = [ac for ac in get_academic_years() if ac['name'] == name]
        if len(l) == 0: return None
        hash_years[name] = l[0]
    return hash_years[name]

def get_edu_id(name):
    if not name in edu_ids.keys(): return None
    return edu_ids[name]

def get_acYear_id(name):
    if not name in hash_years.keys(): return None
    return hash_years[name]['id']
