import pandas as pd
from openai import OpenAI

# Initialize the OpenAI client

client = OpenAI(api_key='your_api_key')  # Replace with your OpenAI API key

# Load the CSV file
csv_file = r"E:\master_clauses.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Function to summarize laws into short wordings
def summarize_laws(laws):
    prompt = f"Summarize the following laws into short, concise wordings:\n\n{laws}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the appropriate model
        messages=[
            {"role": "system", "content": "You are a legal expert. Summarize the laws into short, concise wordings."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,  # Limit the response to short wordings
        temperature=0.8
    )
    
    return response.choices[0].message.content.strip()

# Iterate over the 'Applicable_Laws' column
for index, row in df.iterrows():
    applicable_laws = row['Applicable_Laws']
    
    # Summarize the applicable laws into short wordings
    summarized_laws = summarize_laws(applicable_laws)
    
    print(f"Summarized Laws for Contract ID {row['Applicable_Laws']}:\n{summarized_laws}\n")
    
    # Save the summarized laws back to the DataFrame
    df.at[index, 'Summarized_Laws'] = summarized_laws

# Save the updated DataFrame to a new CSV file
output_file = r"E:\master_clauses.csv"  # Replace with your desired output file path
df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")