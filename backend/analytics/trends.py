from sqlalchemy import func
from models import Paper
def publication_trends(db):
    rows=db.query(Paper.publication_year,func.count(Paper.id)).filter(Paper.publication_year.isnot(None)).group_by(Paper.publication_year).order_by(Paper.publication_year).all()
    return [{"year":int(y),"count":int(c)} for y,c in rows]
def category_distribution(db,limit=10):
    rows=db.query(Paper.category,func.count(Paper.id)).filter(Paper.category.isnot(None),Paper.category!="").group_by(Paper.category).order_by(func.count(Paper.id).desc()).limit(limit).all()
    return [{"category":c,"count":int(n)} for c,n in rows]
