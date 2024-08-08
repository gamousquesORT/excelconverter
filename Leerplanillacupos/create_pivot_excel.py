import pandas as pd

# Create a DataFrame with some data
data = {
    'Column1': [1, 2, 3, 4],
    'Column2': ['A', 'B', 'C', 'D']
}
df = pd.DataFrame(data)

# Write the DataFrame to a new Excel file
output_file = 'new_excel_file.xlsx'
df.to_excel(output_file, index=False)

print(f"New Excel file created: {output_file}")