# Architecture
React/Vite -> FastAPI REST -> service layer -> SQLAlchemy ORM -> PostgreSQL.
The retrieval layer loads paper metadata and abstracts from PostgreSQL and ranks them using Boolean, TF-IDF/cosine, BM25, Sentence Transformer semantic, or hybrid methods. Analytics applies LDA topic modelling and TF-IDF K-Means clustering. OpenAlex ingestion reconstructs inverted-index abstracts and imports paper/author metadata transactionally.
