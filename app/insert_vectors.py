# %%

from datetime import datetime

import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file
df = pd.read_csv("E:\AI-compliance-regulator\data\mydataset.csv", sep=",")
#df = pd.read_excel("../data/Datasets_R.xlsx")
df.head()


# Prepare data for insertion
def prepare_record(row):
    """Prepare a record for insertion into the vector store.

    This function creates a record with a UUID version 1 as the ID, which captures
    the current time or a specified time.

    Note:
        - By default, this function uses the current time for the UUID.
        - To use a specific time:
          1. Import the datetime module.
          2. Create a datetime object for your desired time.
          3. Use uuid_from_time(your_datetime) instead of uuid_from_time(datetime.now()).

        Example:
            from datetime import datetime
            specific_time = datetime(2023, 1, 1, 12, 0, 0)
            id = str(uuid_from_time(specific_time))

        This is useful when your content already has an associated datetime.
    """
    # content=f"Category: {row['Category']}\nJob Description: {row['Job Description']}\nAcceptance: {row['Acceptances']}\nResume: {row['Resume']}"cont
    # content = f"JD NAME: {row['JD NAME']}\nJob Description: {row['JD']}\nRESUME: {row['RESUME']}\nInterview_Details: {row['Q AND A']}"
    # content = f"Question: {row['question']}\nAnswer: {row['answer']}"
    content = f"Document Name: {row['Document Name']}\nParties: {row['Parties']}\nGoverning Law Country: {row['Governing Law Country']}\ncontact: {row['contract']}\nApplicable Laws: {row['Applicable_Laws']}\nSummarized Laws: {row['Summarized_Laws']}"
    embedding_1 = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "Filename": row['Filename'],
                "Agreement Date": row['Agreement Date'],
                "Effective Date": row['Effective Date'],
                "Expiration Date": row['Expiration Date'],
                "Renewal Term": row['Renewal Term'],
                "Notice Period To Terminate Renewal": row['Notice Period To Terminate Renewal'],
                "Exclusivity": row['Exclusivity'],
                "Post-Termination Services": row['Post-Termination Services'],
                # "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding_1,
        }
    )


records_df = df.apply(prepare_record, axis=1)

records_df['metadata'] = records_df['metadata'].apply(lambda x: {k: (None if pd.isna(v) else v) for k, v in x.items()})
# Create tables and insert data
vec.create_tables()
#iske niche hai nya code
# drop_index_query = f"DROP INDEX IF EXISTS {sa};"
# vec.execute_query(drop_index_query)

# # Create the index
#vec.create_index()
#vec.create_index()  # DiskAnnIndex
vec.upsert(records_df)

# %%