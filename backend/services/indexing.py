from sqlalchemy.orm import Session, joinedload
from models import Paper
from services.text_preprocessing import TextPreprocessor

class PaperCorpus:
    def __init__(self, db: Session):
        self.db = db
        self.preprocessor = TextPreprocessor()
    def documents(self, year_from=None, year_to=None, category=None):
        q = self.db.query(Paper).options(joinedload(Paper.authors))
        if year_from is not None: q = q.filter(Paper.publication_year >= year_from)
        if year_to is not None: q = q.filter(Paper.publication_year <= year_to)
        if category: q = q.filter(Paper.category.ilike(f"%{category}%"))
        papers = q.all()
        docs = [self.preprocessor.process(f"{p.title or ''} {p.abstract or ''}") for p in papers]
        return papers, docs
