
#%%
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from vector_db import ChromaDBHandler
from openai_client import CustomOpenAI

#%%

faq_data= pd.read_csv('faqs.csv')
contents = [f"Q: {row['question']} A: {row['answer']}" for _, row in faq_data.iterrows()]
ids = [f"id_{i}" for i in range(len(contents))]
# Convert to a list of dictionaries
documents = [{"id": doc_id, "content": content, "metadata": {"source": "car_faq_data"}} for doc_id, content in zip(ids, contents)]


# %%
# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Initialize ChromaDBHandler
db_handler = ChromaDBHandler(api_key=OPENAI_API_KEY, persist_directory="./chroma_db")

# Create or load a collection
collection_name = "faq_collection"
db_handler.create_or_load_collection(collection_name)

# Add documents to the collection
#db_handler.add_documents(documents)


#%%

# Query the collection
query_text = "What is car insurance?"
results = db_handler.query(query_text, n_results=5)

# Format the retrieved results into a context string
retrieved_context = "\n".join([f"Document {i+1}: {result['content']}" for i, result in enumerate(results)])

# Create a prompt for the OpenAI model
system_message ="You are an AI assistant. Use the following context to answer the question:"

prompt = f"""
Context:
{retrieved_context}

Question:
{query_text}

Answer:
"""
#%%

# Use CustomOpenAI to generate a response
openai_handler = CustomOpenAI(api_key=OPENAI_API_KEY)
client = openai_handler.get_or_create_client()

# Generate the response
messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Use the appropriate engine
    messages=messages,
    max_tokens=200,
    temperature=0.7
)

# Print the response
print(response.choices[0].message.content)

# %%

