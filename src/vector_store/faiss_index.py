from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
import os
import pickle

def create_faiss_index(documents, embedding_model):
    vector_store = FAISS.from_documents(documents, embedding_model)
    return vector_store

def save_faiss_index(vector_store, folder_path, index_name="index"):
    os.makedirs(folder_path, exist_ok=True)
    vector_store.save_local(folder_path, index_name)

def load_faiss_index(folder_path, embedding_model, index_name="index"):
    vector_store = FAISS.load_local(
        folder_path, 
        embedding_model, 
        index_name,
        allow_dangerous_deserialization=True
    )
    return vector_store
