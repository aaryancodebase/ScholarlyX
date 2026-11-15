
# ResearchLens

### Hybrid Academic Research Retrieval & Text Analytics Platform

ResearchLens is an academic research discovery platform designed to retrieve, rank, and analyze computer science research papers using traditional Information Retrieval techniques and modern semantic search methods.

## Features

### Information Retrieval
- Boolean Retrieval
- Inverted Index
- TF-IDF and Cosine Similarity
- BM25 Ranking
- Semantic Search
- Hybrid Search using Reciprocal Rank Fusion

### Text Analytics
- Text Preprocessing
- Topic Modelling using LDA
- Document Clustering using K-Means
- Research Trend Analysis
- Extractive Summarization

### Evaluation
- Precision@K
- Recall@K
- F1-score
- Mean Average Precision (MAP)
- Normalized Discounted Cumulative Gain (NDCG)

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Text Processing | NLTK, spaCy |
| Machine Learning | Scikit-learn |
| Semantic Search | Sentence Transformers |
| Vector Search | FAISS |
| Topic Modelling | Gensim |

## Project Structure

```text
ResearchLens/
├── backend/
├── frontend/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── indexes/
│   └── benchmarks/
├── docs/
├── scripts/
├── .gitignore
└── README.md
```

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Configure your `.env` file using `.env.example`.

Start the backend:

```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Status

Under active development.
