from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.database import get_db
from models import Paper,Author,SearchQuery
from analytics.trends import publication_trends,category_distribution
from analytics.topic_modeling import discover_topics
from analytics.clustering import cluster_documents
from services.indexing import PaperCorpus
router=APIRouter(prefix="/api/v1/analytics",tags=["Analytics"])
@router.get("/overview")
def overview(db:Session=Depends(get_db)):
    return {"total_papers":db.query(func.count(Paper.id)).scalar() or 0,
        "total_authors":db.query(func.count(Author.id)).scalar() or 0,
        "total_searches":db.query(func.count(SearchQuery.id)).scalar() or 0,
        "average_citations":round(float(db.query(func.avg(Paper.citation_count)).scalar() or 0),2),
        "yearly_publications":publication_trends(db),"top_categories":category_distribution(db)}
@router.get("/topics")
def topics(db:Session=Depends(get_db),count:int=6):
    _,docs=PaperCorpus(db).documents()
    return {"topics":discover_topics(docs,max(2,min(count,12))),"documents_used":len(docs)}
@router.get("/clusters")
def clusters(db:Session=Depends(get_db),count:int=5):
    _,docs=PaperCorpus(db).documents()
    return {"clusters":cluster_documents(docs,max(2,min(count,10))),"documents_used":len(docs)}
