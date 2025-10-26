#!/usr/bin/env python

import os
import sys
import argparse

# Add root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from validation import validate
from migration import migrate

app = create_app()

def get_dypa_type_from_file_name(file):
    if 'saek' in file: return 3
    if 'pepas' in file: return 2
    if 'epas' in file: return 1
    if 'amea_ath' in file: return 95
    if 'amea_thes' in file: return 33
    return None

with app.app_context():
    #file_path = "../data/epas.xlsx"

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Excel file name in /data dir. No extension")
    args = parser.parse_args()
    if not args.file :
        print("File name arg is required")
        exit()
    
    dypaType = get_dypa_type_from_file_name(args.file)
    if not dypaType :
        print("Could not get dypa type from file name")
        exit()
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(base_dir, 'data', f'{args.file}.xlsx')
    if not os.path.exists(file_path):
        print("File does not exist: ", file_path)
        exit()
    data = validate.validate_school(dypaType, file_path)
    errors = data['errors']

    sections = data['section_students']
    #print(data)
    error_sections = []
    if sections:
        #error_sections = [s for s in sections if not s['exist']]
        error_sections = [s for k,s in sections.items() if not s['exist']]
        sections = [s for k,s in sections.items() if s['exist']]

    if not errors and (sections and not error_sections):
        #✅❌
        print("✅ Everything seems OK.")
        print("Running migration")
        if input("continue to migration ? (y/n): ") == 'y':
             migrate.migrate_school(dypaType, file_path)
    else:
        exist_students = data['existing_students'] if 'existing_students' in data.keys() else None
        if errors: print("❌ Errors found:")
        for err in errors:
            print(" -", err)
        if error_sections:  print("❌Sections not found:")
        for err in error_sections:
            print(" -", err['name'])
        if exist_students:  
            print("❌Students exist:")
            for err in exist_students:
                print(" -", err)
