import pandas as pd
import os

# Path to the CSV file
csv_file_path = r"E:\master_clauses.csv"

# Path to the folder containing the text files
text_files_folder_path = r"C:\Users\acer\Downloads\archive (1)\CUAD_v1\full_contract_txt"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Initialize a new column 'contract' to store the content of the text files
df['contract'] = ''

# Function to remove .pdf or .PDF extension from the filename
def remove_pdf_extension(filename):
    if filename.lower().endswith('.pdf'):
        return filename[:-4]
    return filename

# Iterate through the DataFrame rows
for index, row in df.iterrows():
    file_name = row['Filename']  # Assuming the column with file names is named 'Filename'
    file_name_without_extension = remove_pdf_extension(file_name)
    file_path = os.path.join(text_files_folder_path, file_name_without_extension + '.txt')

    # Debugging statements
    print(f"Processing file: {file_name}")
    print(f"File name without extension: {file_name_without_extension}")
    print(f"Constructed file path: {file_path}")

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the content of the text file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # Add the content to the 'contract' column
        df.at[index, 'contract'] = content
    else:
        print(f"File {file_path} does not exist.")

# Save the updated DataFrame back to a CSV file
output_csv_file_path = r"E:\master_clauses.csv"
df.to_csv(output_csv_file_path, index=False)

print(f"Updated CSV file saved to {output_csv_file_path}")
