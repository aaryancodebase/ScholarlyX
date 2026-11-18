import time
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import SearchQuery
from schemas.search import SearchRequest
from services.indexing import PaperCorpus
from services.boolean_retrieval import boolean_search, normalize_boolean_query
from services.tfidf import rank_tfidf
from services.bm25 import rank_bm25
from services.semantic_search import rank_semantic
from services.hybrid_search import rank_hybrid

router=APIRouter(prefix="/api/v1",tags=["Search"])
@router.post("/search")
def search(payload:SearchRequest,db:Session=Depends(get_db)):
    started=time.perf_counter()
    corpus=PaperCorpus(db)
    papers,docs=corpus.documents(payload.year_from,payload.year_to,payload.category)
    if not papers:return {"query":payload.query,"method":payload.method,"total":0,"took_ms":0,"results":[]}
    query=corpus.preprocessor.process(payload.query)
    try:
        if payload.method=="boolean":
            ranked=[(i,1.0) for i in boolean_search(normalize_boolean_query(payload.query,corpus.preprocessor),docs)]
        elif payload.method=="tfidf": ranked=rank_tfidf(query,docs)
        elif payload.method=="bm25": ranked=rank_bm25(query,docs)
        elif payload.method=="semantic": ranked=rank_semantic(payload.query,[f"{p.title or ''}. {p.abstract or ''}" for p in papers])
        else: ranked=rank_hybrid(query,docs)
    except Exception as exc:
        raise HTTPException(status_code=422,detail=f"Search failed: {exc}")
    results=[]
    for idx,score in ranked[:payload.limit]:
        p=papers[idx]
        results.append({"id":str(p.id),"title":p.title,"abstract":p.abstract,"year":p.publication_year,
            "citations":p.citation_count or 0,"category":p.category,"doi":p.doi,"url":p.paper_url,
            "authors":[a.name for a in p.authors],"score":round(float(score),6),
            "explanation":f"Ranked using {payload.method.upper()}."})
    elapsed=round((time.perf_counter()-started)*1000,2)
    db.add(SearchQuery(query_text=payload.query,search_type=payload.method,results_count=len(results)))
    db.commit()
    return {"query":payload.query,"method":payload.method,"total":len(ranked),"took_ms":elapsed,"results":results}
