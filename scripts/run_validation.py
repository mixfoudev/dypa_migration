#!/usr/bin/env python

import os
import sys
import argparse

# Add root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from validation import validate

app = create_app()

with app.app_context():
    #file_path = "../data/epas.xlsx"

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Excel file name in /data dir. No extension")
    args = parser.parse_args()
    if not args.file :
        print("File name arg is required")
        exit()
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(base_dir, 'data', f'{args.file}.xlsx')
    
    errors= validate.validate_school('1', file_path)['errors']

    if not errors:
        print("✅ Everything seems OK.")
    else:
        print("❌ Errors found:")
        for err in errors:
            print(" -", err)
