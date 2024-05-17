import pandas as pd
import os
import re

dir_name = "./data/"
file_name = "030323.xlsx"
output_excel_file = "output_" + file_name  # Replace with your desired output file path

# Use os.path.join to construct the file path
file_path = os.path.join(dir_name, file_name)

# Now you can use this file path in a platform-independent manner
df = pd.read_excel(file_path, sheet_name="data")

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

# Initialize an empty DataFrame to store filtered rows
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
            continue

# Create a DataFrame from the filtered rows
filtered_df = pd.DataFrame(filtered_rows)

# Write the filtered DataFrame to a new Excel sheet
filtered_df.to_excel(output_excel_file, index=False)

print("Filtered rows with new columns written to", output_excel_file)