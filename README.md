# SHL Assessment Recommender System

A **Retrieval-Augmented Generation (RAG)** application designed to intelligently recommend **SHL assessments** based on user queries. The system combines **semantic vector search** with **Google’s Gemini LLM** to deliver context-aware, accurate, and explainable assessment recommendations.

This project is built with a production-oriented mindset, focusing on clean architecture, comprehensive evaluation, and fallback reliability.

**[🚀 View Live Application](https://shl-assessment-recommender-system-bko69cxu4wbqgy9tfh5put.streamlit.app)**

---

## 🚀 Key Features

*   **Intelligent Semantic Search**
    Utilizes **SentenceTransformers (all-MiniLM-L6-v2)** to comprehend user intent beyond elementary keyword matching, ensuring high-fidelity retrieval.

*   **AI-Powered Recommendations**
    Integrates **Google Gemini 1.5 Flash** to generate natural-language justifications, explaining precisely why specific assessments are recommended for a given context.

*   **Robust Data Pipeline**
    *   Supports versatile input formats including **JSON, CSV, and Excel**.
    *   Automated normalization of column schemas.
    *   Metadata extraction (e.g., duration, complexity) from unstructured text via regex pattern matching.

*   **Hybrid Output Architecture**
    *   **Human-readable:** Formatted summaries designed for end-user consumption.
    *   **Machine-readable:** Structured JSON output optimized for API consumption or downstream integration.

*   **Evaluation Module**
    Includes built-in utilities to calculate **Recall@K** metrics, validating retrieval accuracy using a rigorous known-item search methodology.

*   **Resilient Design**
    Implements a fallback mechanism that returns structured semantic search results even during LLM unavailability or rate-limiting events.

---

## 🧠 System Architecture

1.  **Ingestion Layer**
    Ingests and sanitizes the SHL product catalog, creating a consolidated text corpus for embedding generation.

2.  **Embedding & Vector Store**
    Transforms assessment descriptions into dense vectors using SentenceTransformers, persisting them in a **FAISS** index for high-performance similarity search.

3.  **RAG Engine**
    Retrieves the most semantically relevant assessments and augments the context window before invoking the Gemini LLM for final response synthesis.

4.  **Evaluation Module**
    Quantifies retrieval quality via Recall@K metrics and exports detailed performance reports.

---

## 📁 Project Structure

```
shl/
├── data/                   # Data storage
│   ├── shl_products.json   # Source assessment catalog
│   └── faiss_index/        # FAISS vector index
├── outputs/                # Generated outputs (JSON / CSV)
├── src/                    # Source code
│   ├── config.py           # Global configuration
│   ├── embeddings/         # Embedding logic
│   ├── evaluation/         # Recall@K evaluation scripts
│   ├── ingestion/          # Data loading and cleaning
│   └── rag/                # Core RAG engine
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (API keys)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/adityat22/SHL-Assessment-Recommender-System.git
cd SHL-Assessment-Recommender-System
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**Mac / Linux**

```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Usage

### 🔹 Run the Recommendation Engine

To test the RAG pipeline with a sample query:

```bash
python src/rag/rag_engine.py
```

This executes a test query defined in the `__main__` block and outputs:

* A human-readable recommendation summary
* A structured JSON response

---

### 🔹 Run Retrieval Evaluation (Recall@K)

To evaluate semantic search performance:

```bash
python src/evaluation/run_eval.py
```

Evaluation results will be saved to:

```
outputs/evaluation_results.csv
```

---

## ⚙️ Configuration

Key configuration options can be modified in `src/config.py`:

* `CATALOG_PATH` – Path to the SHL catalog file
* `TOP_K` – Number of assessments to retrieve (default: 10)
* `EMBEDDING_MODEL` – SentenceTransformer model name
* `GEMINI_MODEL` – Gemini LLM version used for generation

---

## 🧪 Evaluation Methodology

The system uses **Recall@K** to evaluate retrieval accuracy:

* Measures whether the correct assessment appears in the top **K** retrieved results
* Suitable for known-item and recommendation-style search systems
* Helps validate embedding quality and retrieval logic

---

## 🛠 Tech Stack

* **Language:** Python 3.12
* **Orchestration:** LangChain
* **Vector Database:** FAISS
* **LLM:** Google Gemini 1.5 Flash
* **Embeddings:** SentenceTransformers (HuggingFace)
* **Data Processing:** Pandas

---

## 📌 Use Cases

* Automated SHL assessment recommendation from job descriptions
* HR-tech and recruitment platforms
* Skill-based assessment discovery systems
* GenAI-powered search and recommendation demos

