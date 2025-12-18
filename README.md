# SHL Assessment Recommendation Engine

This project is an AI-powered recommendation engine for SHL assessments. It uses a RAG (Retrieval-Augmented Generation) architecture to recommend the best assessments based on user needs.

## Features

-   **Data Ingestion**: Scrapes and parses SHL product catalog data.
-   **Vector Store**: Uses FAISS for efficient similarity search.
-   **Embeddings**: Uses local HuggingFace embeddings (`all-MiniLM-L6-v2`) for privacy and reliability.
-   **RAG Engine**: Retrieves relevant assessments and generates recommendations using Google Gemini (with fallback to raw results if API is unavailable).
-   **API**: FastAPI endpoint for easy integration.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file with your API key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

## Usage

### 1. Ingest Data (if needed)
The data is already scraped and ingested. To re-run:
```bash
python src/ingestion/load_catalog.py
```

### 2. Run the API
Start the FastAPI server:
```bash
python -m uvicorn src.api.main:app --reload
```

### 3. Get Recommendations
Send a POST request to `/recommend`:
```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
     -H "Content-Type: application/json" \
     -d '{"query": "I need a python coding test for a senior developer"}'
```

## Project Structure

-   `data/`: Stores scraped data and the FAISS index.
-   `src/ingestion/`: Scripts for loading data into the vector store.
-   `src/rag/`: The core RAG engine logic.
-   `src/api/`: FastAPI application.
-   `src/embeddings/`: Embedding model configuration.
