import pandas as pd
import os
import re
from check_valid_file_and_data_properties import valid_excel_file
from check_valid_file_and_data_properties import get_dataframe_for_enrollment_sheet
from name_unnamed_columns import rename_unamed_columns
file_path: str = "./data/"

# List of Materia values to filter
materia_list = [
    "Arq. de soft. en la práctica" ,
    "Arquitectura de software" ,
    "Arq.de soft.en la práctica" ,
    "Arquitecturas Serverless" ,
    "Desarrollo de prod. base Tec." ,
    "Diseño de aplicaciones 1" ,
    "Diseño de aplicaciones 2" ,
    "Fundamentos de Ing de software" ,
    "Ingeniería de software ágil 1" ,
    "Ingeniería de software ágil 2" ,
    " Calidad en software" ,
    "Interacción humano-computadora" ,
    "Tec. de negoc. para equip proy" ,
    "Hab de equipo en desar de soft" ,
    " Gestión de com, confl en proy" ,
    "Diseño centrado en el usuario"
]



files = os.listdir(file_path)

valid_columns_to_split = {
    "Ins/Cupo": "/" ,
    "Ins_Cupo": "/"
}

def is_string(cell):
    return isinstance(cell, str)

inline_text_date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{2}\b'
inline_text_date_regex = re.compile(inline_text_date_pattern)

file_date_pattern = r'\b(\d{2})(\d{2})(\d{2})\b|\b(\d{2})\s(\d{2})\s(\d{2})\b'
file_date_regex = re.compile(file_date_pattern)



def select_split_char_named():
    global split_char , split_column
    if 'Ins/Cupo' in df.columns:
        split_char = valid_columns_to_split['Ins/Cupo']
        split_column = 'Ins/Cupo'
    elif 'Ins_Cupo' in df.columns:
        split_char = valid_columns_to_split['Ins_Cupo']
        split_column = 'Ins_Cupo'


def insert_course_session_named():
    global inscriptos , cupos , row_index
    inscriptos , cupos = row[split_column].split(split_char)
    # Add Inscriptos and Cupos columns to the row
    row['Inscriptos'] = inscriptos.strip()  # remove leading/trailing spaces
    row['Cupos'] = cupos.strip()
    row['Fecha'] = date_to_insert.strip()  # remove leading/trailing spaces
    # Append the row to the filtered_rows list
    filtered_rows.append(row)



def set_date_to_insert_named():
    global date_match , date_to_insert
    # define date based on file name
    date_match = file_date_regex.search(file)
    if date_match:
        date_to_insert = date_match.group()


def insert_date_to_row_unnamed():
    global date_match , date_to_insert , row_index
    fecha_str = df.iloc[row_index , 0]
    date_match = inline_text_date_regex.search(df.iloc[row_index , 0])
    if date_match:
        date_to_insert = date_match.group()
    row_index = row_index + 1


def init_file_processing_variables():
    global split_char , split_column , materia_marker_found , row_index , date_to_insert , named_column_mode , eof_reached
    split_char = None
    split_column = None
    materia_marker_found = False
    row_index = 0
    date_to_insert = None
    named_column_mode = False
    eof_reached = False


def generate_output_file():
    # Create a DataFrame from the filtered rows
    filtered_df = pd.DataFrame(filtered_rows)
    output_excel_file = "output_" + file
    # Write the filtered DataFrame to a new Excel sheet
    filtered_df.to_excel(output_excel_file , index=False)
    print("Filtered rows with new columns written to" , output_excel_file)


# Iterate over each file in the directory
for file in files:

    init_file_processing_variables()
    filtered_rows = []

    if valid_excel_file(file):
        try:
            # Get the DataFrame for the file
            df = get_dataframe_for_enrollment_sheet(file , file_path)
            rename_unamed_columns(df)
            select_split_char_named()
            set_date_to_insert_named() # use default date found in file

        except ValueError as e:
            print(e)
            continue

        # Iterate over each row
        for index , row in df.iterrows():
            if eof_reached:
                break

            # Check if 'Id' column is empty or NaN
            if row.isnull().all():
                row_index = row_index + 1
                continue

            # Convert the list to lower case and strip spaces
            cell_value = df.iloc[row_index,0]
            if type(cell_value) == str and "LISTADO" in df.iloc[row_index,0] :
                insert_date_to_row_unnamed()
                continue


            if 'Tipo dictado' in df.columns:
                if 'Se imprimieron'in row['Tipo dictado']:
                    eof_reached = True
                    continue

            nombre_materia = row['Materia']
            if nombre_materia.strip() in materia_list:
                try:
                    insert_course_session_named()
                except ValueError:
                    # If splitting fails, print a message and continue iterating
                    print("Cannot split Ins_Cupos value in row:" , index)
                    break

        generate_output_file()
