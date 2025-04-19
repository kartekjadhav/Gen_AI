from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from openai import OpenAI


load_dotenv()
client = OpenAI()

pdf_path = Path(__file__).parent / 'Introduction_to_Python_Programming_-_WEB.pdf'



#Pdf document loader
loader = PyPDFLoader(pdf_path)
docs = loader.load()


#Text splitting into managable chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)

split_docs = text_splitter.split_documents(documents=docs)


# Creating embedder
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#Storing in Vector DB (Qdrant)

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedder,
    collection_name="my_langchain",
    url="http://localhost:6333",
)

# vector_store.add_documents(documents=split_docs)


print("INGESTION DONE!!")



# User query

query = "I am interested to know about the author of this book."

print("QUERY -> ",query)

relevant_chunks = vector_store.similarity_search(
    query=query
)

# print("RELEVANT_CHUNKS -> ",relevant_chunks)

SYSTEM_PROMPT = f"""
You are an helpful AI assistant, who resolves user's query based on relevant_chunks.

relevant_chunks = {relevant_chunks} 

"""

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
)

print("RESPONSE -> ",response.choices[0].message.content)


