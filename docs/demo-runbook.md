# Viva / demo sequence
1. Start PostgreSQL and verify the researchlens database.
2. Start backend with `uvicorn main:app --reload` from backend.
3. Verify `/api/v1/health` and open `/docs`.
4. Start frontend with `npm run dev` from frontend.
5. Import 100–250 papers using Dataset Manager.
6. Search one query with BM25, TF-IDF, Boolean and Hybrid; compare rankings.
7. Open Text Analytics to show LDA topics and K-Means clusters.
8. Explain that semantic retrieval downloads its model at first use.
