from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings



file_path = Path(__file__).parent / "Financial_Sample.xlsx"
print("FILE PATH -> ",file_path)

load_dotenv()
client = OpenAI()

# # Data loading
# loader = UnstructuredExcelLoader(file_path)
# docs = loader.load()

# print("LOADING DONE")

# # Splitting
# text_splitters = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200
# )

# split_docs = text_splitters.split_documents(docs)

# print("CHUNCKING DONE")


#Embedder
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#Storing in Vector DB
vector_store = QdrantVectorStore.from_existing_collection(
    collection_name="excel_collection",
    embedding=embedder
)

# vector_store.add_documents(documents=split_docs)

# print("INGESTION IS COMPLETED!")




#### USER QUERY

print("RUNNING USER QUERY")


user_query = "Tell me performance of product Carretera in Midmarket France in JUne 2014"

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
