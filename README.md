# ScholarlyX

### Hybrid Academic Research Retrieval & Text Analytics Platform

ScholarlyX is an academic research discovery platform designed to retrieve, rank, and analyze computer science research papers using traditional Information Retrieval techniques and modern semantic search methods.

It combines multiple retrieval algorithms with machine learning and natural language processing techniques to help users discover relevant academic publications, explore research topics, and analyze emerging trends in computer science.

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
ScholarlyX/
├── backend/
│   ├── api/
│   ├── core/
│   ├── ingestion/
│   ├── models/
│   ├── services/
│   ├── evaluation/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── vite.config.js
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

### Prerequisites

- Python 3.11
- Node.js and npm
- PostgreSQL
- Git

### Backend Setup

Clone the repository:

```bash
git clone https://github.com/aaryancodebase/ScholarlyX.git
cd ScholarlyX
```

Navigate to the backend:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure your `.env` file using `.env.example` and provide your PostgreSQL database credentials.

Initialize the database and start the backend:

```bash
python init_db.py
python -m uvicorn main:app --reload
```

Backend API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

Open a separate terminal and navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL provided by Vite, normally:

```text
http://localhost:5173
```

## Project Status

Under active development.

## Author

**Aaryan Bose**

GitHub: [@aaryancodebase](https://github.com/aaryancodebase)