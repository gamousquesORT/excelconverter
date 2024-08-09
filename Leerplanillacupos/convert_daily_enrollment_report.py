import pandas as pd
import os
from check_valid_file_and_data_properties import valid_excel_file
from check_valid_file_and_data_properties import get_dataframe_for_enrollment_sheet

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
    "Ins_Cupo": "_"
}



# Iterate over each file in the directory
for file in files:
    split_char = None
    split_column = None
    materia_marker_found = False
    row_index = 0
    # Check if the file is an Excel file
    if valid_excel_file(file):
        try:
            # Get the DataFrame for the file
            df = get_dataframe_for_enrollment_sheet(file , file_path)
        except ValueError as e:
            print(e)
            continue

        #Initialize an empty DataFrame to store filtered rows
        filtered_rows = []

        # Iterate over each row
        for index , row in df.iterrows():


            # Check if 'Id' column is empty or NaN
            if row.isnull().all():
                row_index = row_index + 1
                continue

            print("index is:", row_index)
            print("the excel row is:")
            print(df.iloc[row_index])


            print("cell value is:")
            print(df.iloc[row_index, 3])

            # Convert the list to lower case and strip spaces
            if "LISTADO DE INSCRTIPTOS" in row.values:
                row_index = row_index + 1
                continue

            if 'Materia' in row.values and not materia_marker_found:
                materia_marker_found = True
                for value in row.values:
                    if value in valid_columns_to_split.keys():
                        split_char = valid_columns_to_split[value]
                        split_column = str(value)

                        break
                row_index = row_index + 1
                continue
            if materia_marker_found:
                nombre_materia = df.iloc[row_index , 3]
                if nombre_materia.strip() in materia_list:
                    try:
                        inscriptos , cupos = df.iloc[row_index, 6].split(split_char)
                        # Add Inscriptos and Cupos columns to the row
                        row['Inscriptos'] = inscriptos.strip()  # remove leading/trailing spaces
                        row['Cupos'] = cupos.strip()
                        # Append the row to the filtered_rows list
                        filtered_rows.append(row)
                    except ValueError:
                        # If splitting fails, print a message and continue iterating
                        print("Cannot split Ins_Cupos value in row:" , index)
                        break
            row_index = row_index + 1

        # Create a DataFrame from the filtered rows
        filtered_df = pd.DataFrame(filtered_rows)

        output_excel_file = "output_" + file  # Replace with your desired output file path

        # Write the filtered DataFrame to a new Excel sheet
        filtered_df.to_excel(output_excel_file , index=False)

        print("Filtered rows with new columns written to" , output_excel_file)
