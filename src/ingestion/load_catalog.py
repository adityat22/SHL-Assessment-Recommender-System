import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config import PARSED_DATA_PATH, DATA_DIR
from src.embeddings.embedder import get_embedding_model
from src.vector_store.faiss_index import create_faiss_index, save_faiss_index
from src.utils.text import create_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter

def ingest_data():
    print("Loading parsed data...")
    if not os.path.exists(PARSED_DATA_PATH):
        print(f"Error: {PARSED_DATA_PATH} not found. Run parser first.")
        return

    with open(PARSED_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} items.")
    
    raw_documents = create_documents(data)
    
    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    documents = text_splitter.split_documents(raw_documents)
    print(f"Created {len(documents)} document chunks.")
    
    print("Initializing embedding model...")
    try:
        embeddings = get_embedding_model()
    except Exception as e:
        print(f"Error initializing embeddings: {e}")
        return

    print("Creating FAISS index with batching (this may take a while)...")
    import time
    
    batch_size = 2
    delay = 10
    
    vector_store = None
    
    try:
        total_docs = len(documents)
        for i in range(0, total_docs, batch_size):
            batch = documents[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size} ({len(batch)} docs)...")
            
            retry_count = 0
            max_retries = 5
            while retry_count < max_retries:
                try:
                    if vector_store is None:
                        vector_store = create_faiss_index(batch, embeddings)
                    else:
                        vector_store.add_documents(batch)
                    break
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        wait_time = (2 ** retry_count) * 5
                        print(f"Rate limit hit. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        retry_count += 1
                    else:
                        raise e
            
            if retry_count == max_retries:
                print("Max retries exceeded. Aborting.")
                return

            if i + batch_size < total_docs:
                time.sleep(delay)
        
        index_path = os.path.join(DATA_DIR, "faiss_index")
        save_faiss_index(vector_store, index_path)
        print(f"Successfully saved FAISS index to {index_path}")
        
    except Exception as e:
        print(f"Error creating/saving index: {e}")

if __name__ == "__main__":
    ingest_data()
