import pandas as pd
import os
from check_excel_file_properties import check_worksheet

dir_name = "./data/"

# List of Materia values to filter
materia_list = [
    "Arq. de soft. en la práctica",
    "Arquitectura de software",
    "Arquitecturas Serverless",
    "Desarrollo de prod. base Tec.",
    "Diseño de aplicaciones 1",
    "Diseño de aplicaciones 2",
    "Fundamentos de Ing de software",
    "Ingeniería de software ágil 1",
    "Ingeniería de software ágil 2",
    " Calidad en software",
    "Interacción humano-computadora",
    "Tec. de negoc. para equip proy",
    "Hab de equipo en desar de soft"
]

files = os.listdir ( dir_name )

# Iterate over each file in the directory
for file in files:
    # Check if the file is an Excel file
    if file.endswith ( ".xlsx" ) or file.endswith ( ".xls" ):
        # Construct the full file path
        file_path = os.path.join ( dir_name , file )
        print("Reading file:", file_path)
        # Read the Excel file into a DataFrame

        #df = pd.read_excel(file_path, sheet_name="data")
        df = pd.read_excel(file_path)
        try:
            check_worksheet(pd, file_path)
        except (ValueError) as e:
            print("Error in worksheet format"+e.args[0])
            continue

        #Initialize an empty DataFrame to store filtered rows
        filtered_rows = []

        # Iterate over each row
        for index, row in df.iterrows():
            # Check if 'Id' column is empty or NaN
            if pd.isnull(row['Id']):
                break  # Stop the loop

            # Convert the list to lower case and strip spaces
            materia_list = [m.lower().strip() for m in materia_list]

            # In the loop
            if row['Materia'].lower().strip() in materia_list:
                # Try splitting the value in Ins_Cupos
                try:
                    inscriptos, cupos = row['Ins_Cupo'].split('/')
                    # Add Inscriptos and Cupos columns to the row
                    row['Inscriptos'] = inscriptos.strip()  # remove leading/trailing spaces
                    row['Cupos'] = cupos.strip()
                    # Append the row to the filtered_rows list
                    filtered_rows.append(row)
                except ValueError:
                    # If splitting fails, print a message and continue iterating
                    print("Cannot split Ins_Cupos value in row:", index)
                    break

        # Create a DataFrame from the filtered rows
        filtered_df = pd.DataFrame(filtered_rows)

        output_excel_file = "output_" + file  # Replace with your desired output file path

        # Write the filtered DataFrame to a new Excel sheet
        filtered_df.to_excel(output_excel_file, index=False)

        print("Filtered rows with new columns written to", output_excel_file)

