import os
import numpy as np
_model=None
def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model=SentenceTransformer(os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2"))
    return _model
def rank_semantic(query,documents):
    if not documents: return []
    model=_get_model()
    vectors=model.encode(documents,normalize_embeddings=True,show_progress_bar=False)
    q=model.encode([query],normalize_embeddings=True,show_progress_bar=False)[0]
    scores=np.dot(vectors,q)
    return sorted(enumerate(scores.tolist()),key=lambda x:x[1],reverse=True)
