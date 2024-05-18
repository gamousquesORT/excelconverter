def check_worksheet(pd, file_path):
    xls = pd.ExcelFile( file_path )

    sheet_names = xls.sheet_names
    if "data" not in sheet_names:
        raise ValueError("Worksheet 'data' not found" + file_path )
