import pandas as pd
from openai import OpenAI

# Initialize the OpenAI client

client = OpenAI(api_key='put_your_api')  # Replace with your OpenAI API key

# Load the CSV file
csv_file = r"E:\master_clauses.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Function to get applicable laws from LLM
def get_applicable_laws(contract_details):
    prompt = f"Given the following contract details, give a list of only exact name of laws that are applicable to such contracts?\n\n{contract_details} response should only have the names"
    
    # Use the new OpenAI API format
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # Use the appropriate model
        messages=[
            {"role": "system", "content": "You are a legal expert. Analyze the contract details and provide the applicable laws."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.8
    )
    
    return response.choices[0].message.content.strip()

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Prepare contract details for the current row
    contract_details = f"""
    contract: {row['contract']}
    Country whose law are applicable : {row['Governing Law Country']}
    Document name: {row['Document Name']}
    Parties: {row['Parties']}
    Agreement Date: {row['Agreement Date']}
    Effective Date: {row['Effective Date']}
    Renewal Term: {row['Renewal Term']}
    Notice Period To Terminate Renewal: {row['Notice Period To Terminate Renewal']}
    Exclusivity: {row['Exclusivity']}
    Post-Termination Services: {row['Post-Termination Services']}
    """
    
    applicable_laws = get_applicable_laws(contract_details)
    
    print(f"Applicable Laws for Contract ID {row['Filename']}:\n{applicable_laws}\n")
    
    # Optionally, save the results back to the DataFrame
    df.at[index, 'Applicable_Laws'] = applicable_laws

# Save the updated DataFrame to a new CSV file
output_file = csv_file
df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
