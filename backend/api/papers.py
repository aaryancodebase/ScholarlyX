from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session,joinedload
from core.database import get_db
from models import Paper
from services.summarization import extractive_summary
router=APIRouter(prefix="/api/v1/papers",tags=["Papers"])
@router.get("")
def list_papers(db:Session=Depends(get_db),page:int=Query(1,ge=1),limit:int=Query(20,ge=1,le=100)):
    q=db.query(Paper).options(joinedload(Paper.authors)); total=q.count()
    rows=q.order_by(Paper.publication_year.desc().nullslast(),Paper.citation_count.desc()).offset((page-1)*limit).limit(limit).all()
    return {"total":total,"page":page,"limit":limit,"items":[{"id":str(p.id),"title":p.title,"year":p.publication_year,"citations":p.citation_count or 0,"category":p.category,"authors":[a.name for a in p.authors],"url":p.paper_url,"doi":p.doi} for p in rows]}
@router.get("/{paper_id}")
def paper_detail(paper_id:str,db:Session=Depends(get_db)):
    p=db.query(Paper).options(joinedload(Paper.authors)).filter(Paper.id==paper_id).first()
    if not p:raise HTTPException(status_code=404,detail="Paper not found")
    return {"id":str(p.id),"title":p.title,"abstract":p.abstract,"summary":extractive_summary(p.abstract or ""),"year":p.publication_year,"citations":p.citation_count or 0,"category":p.category,"authors":[a.name for a in p.authors],"url":p.paper_url,"doi":p.doi}
