from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

DATA_PATH = "Data/"
DB_FAISS_PATH = "vectorstores/db_faiss"

def create_vector_database():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data directory '{DATA_PATH}' not found!")

    # Load PDF documents
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    if not documents:
        raise ValueError("No documents found! Ensure PDFs exist in the Data folder.")

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    if not texts:
        raise ValueError("Text splitting failed! Check the document format.")

    # Load embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Test embedding generation
    test_embedding = embeddings.embed_documents(["test"])
    if not test_embedding:
        raise ValueError("Embeddings not generated! Check model parameters.")

    # Create FAISS vector database
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

    print(f"FAISS database saved at: {DB_FAISS_PATH}")

if __name__ == "__main__":
    create_vector_database()
