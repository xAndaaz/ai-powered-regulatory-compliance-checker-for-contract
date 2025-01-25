import pandas as pd
import os

# Path to the CSV file
csv_file_path = r"E:\master_clauses.csv"

# Path to the folder containing the contracts
contracts_folder_path = r"C:\Users\acer\Downloads\archive (1)\CUAD_v1\full_contract_txt"

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Function to remove .pdf or .PDF extension from the filename
def remove_pdf_extension(filename):
    if filename.lower().endswith('.pdf'):
        print(filename[:-4])
        return filename[:-4]
    return filename

# Function to get the word count of a file
def get_word_count(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return len(content.split())
    except OSError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# Add a new column for word counts
df['Word Count'] = df['Filename'].apply(lambda x: get_word_count(os.path.join(contracts_folder_path, remove_pdf_extension(x) + '.txt')))

# Save the updated DataFrame back to the CSV file
df.to_csv(csv_file_path, index=False)

print("Word counts added to the CSV file.")
