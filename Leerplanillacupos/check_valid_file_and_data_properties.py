import os
import pandas as pd


def valid_excel_file(file):
    if file.endswith(".xlsx") or file.endswith(".xls"):
        return True
    else:
        return False


def get_dataframe_for_enrollment_sheet(file, dir_name):
    # Construct the full file path
    file_path = os.path.join(dir_name, file)
    print( "Reading file:", file)
    xls = pd.ExcelFile (file_path)
    print ("Sheet names:")
    print (xls.sheet_names)

    for sheet_name in xls.sheet_names:
        if "data" in sheet_name or "TDICTADO.RPT" in sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            return df
    raise ValueError("No valid sheet found in file: " + file)