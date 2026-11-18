from core.database import SessionLocal
from models import Paper,Author,paper_authors
from ingestion.openalex import fetch_papers
def _get_author(db,data,cache):
    external_id=data.get("id");name=(data.get("display_name") or "").strip()
    if not name:return None
    key=external_id or name.casefold()
    if key in cache:return cache[key]
    q=db.query(Author)
    author=q.filter(Author.external_id==external_id).first() if external_id else q.filter(Author.name==name).first()
    if author is None:
        author=Author(external_id=external_id,name=name);db.add(author);db.flush()
    cache[key]=author
    return author
def import_papers(limit=100):
    db=SessionLocal();stats={"requested":limit,"fetched":0,"inserted":0,"skipped":0,"authors_linked":0};cache={}
    try:
        rows=fetch_papers(limit);stats["fetched"]=len(rows)
        for item in rows:
            source_id,title,abstract=item.get("id"),item.get("title"),item.get("abstract")
            if not source_id or not title or not abstract:stats["skipped"]+=1;continue
            if db.query(Paper.id).filter(Paper.source_id==source_id).first():stats["skipped"]+=1;continue
            doi=item.get("doi")
            if doi and db.query(Paper.id).filter(Paper.doi==doi).first():stats["skipped"]+=1;continue
            topic=item.get("primary_topic") or {};subfield=topic.get("subfield") or {};oa=item.get("open_access") or {}
            paper=Paper(source_id=source_id,title=title,abstract=abstract,publication_year=item.get("publication_year"),doi=doi,paper_url=oa.get("oa_url"),citation_count=item.get("cited_by_count") or 0,category=subfield.get("display_name") or topic.get("display_name"))
            db.add(paper);db.flush();seen=set()
            for position,authorship in enumerate(item.get("authorships") or []):
                author=_get_author(db,authorship.get("author") or {},cache)
                if author is None or author.id in seen:continue
                seen.add(author.id);db.execute(paper_authors.insert().values(paper_id=paper.id,author_id=author.id,author_position=position));stats["authors_linked"]+=1
            stats["inserted"]+=1
        db.commit();return stats
    except Exception:
        db.rollback();raise
    finally:db.close()
if __name__=="__main__":
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent/".env")
    print(import_papers(int(os.getenv("DATASET_SIZE","1000"))))
