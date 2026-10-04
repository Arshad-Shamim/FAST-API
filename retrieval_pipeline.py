import os
from langchain_chroma import Chroma
# REPLACED: OpenAIEmbeddings with HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Define the open-source model name from Hugging Face
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Smart Environment Path Detection (VS Code vs Kaggle)
IS_KAGGLE = os.path.exists("/kaggle/input")
if IS_KAGGLE:
    persistent_directory = "/kaggle/working/db/chroma_db"
else:
    persistent_directory = "db/chroma_db"

# REPLACED: Load local Hugging Face embeddings instead of OpenAI
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

print(f"Loading vector store from: {persistent_directory}...")
db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "cosine"}  
)

# Search for relevant documents
query = "How much did Microsoft pay to acquire GitHub?"

retriever = db.as_retriever(search_kwargs={"k": 5})

# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={
#         "k": 5,
#         "score_threshold": 0.3  # Only return chunks with cosine similarity ≥ 0.3
#     }
# )

relevant_docs = retriever.invoke(query)

print(f"\nUser Query: {query}")
# Display results
print("--- Context ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")
