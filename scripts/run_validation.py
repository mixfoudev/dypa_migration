#!/usr/bin/env python

import os
import sys
import argparse

# Add root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from validation import validate

app = create_app()

def get_dypa_type_from_file_name(file):
    if 'saek' in file: return 3
    if 'pepas' in file: return 2
    if 'epas' in file: return 1
    if 'amea_ath' in file: return 95
    if 'amea_thess' in file: return 33
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
    
    errors= validate.validate_school(dypaType, file_path)['errors']

    if not errors:
        print("✅ Everything seems OK.")
    else:
        print("❌ Errors found:")
        for err in errors:
            print(" -", err)
