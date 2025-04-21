from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from excel_ingestor import vector_store

load_dotenv()
client = OpenAI()

user_query = "Tell what this excel is all about?"

similar_chunks = vector_store.similarity_search(user_query)

SYSTEM_PROMPT = f"""
You are an helpful AI assistant who resolves user's query based on the given context.

context = {similar_chunks}

"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

print(response.choices[0].message.content)
