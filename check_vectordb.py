from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DB_FAISS_PATH = "vectorstores/db_faiss"

# Load the saved FAISS database safely
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

# Test query
query = "What is the diabetes?"
results = db.similarity_search(query, k=3)  # Retrieve top 3 matches

for i, doc in enumerate(results):
    print(f"Result {i+1}:")
    print(doc.page_content)
    print("=" * 50)
