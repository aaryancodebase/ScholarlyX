import uuid
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, Table, Uuid, func
from sqlalchemy.orm import relationship
from core.database import Base

paper_authors = Table("paper_authors", Base.metadata,
    Column("paper_id", Uuid(as_uuid=True), ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", Uuid(as_uuid=True), ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
    Column("author_position", Integer, default=0))
paper_topics = Table("paper_topics", Base.metadata,
    Column("paper_id", Uuid(as_uuid=True), ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", Uuid(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
    Column("confidence_score", Float, default=0.0))

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(String(150), unique=True, nullable=False, index=True)
    title = Column(Text, nullable=False)
    abstract = Column(Text)
    publication_year = Column(Integer, index=True)
    doi = Column(String(255), unique=True, nullable=True)
    paper_url = Column(Text)
    citation_count = Column(Integer, default=0)
    category = Column(String(150), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    authors = relationship("Author", secondary=paper_authors, back_populates="papers")
    topics = relationship("Topic", secondary=paper_topics, back_populates="papers")

class Author(Base):
    __tablename__ = "authors"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(150), unique=True, nullable=True)
    name = Column(String(255), nullable=False, index=True)
    papers = relationship("Paper", secondary=paper_authors, back_populates="authors")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    model_version = Column(String(100))
    papers = relationship("Paper", secondary=paper_topics, back_populates="topics")

class SearchQuery(Base):
    __tablename__ = "search_queries"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(Text, nullable=False)
    search_type = Column(String(50), nullable=False)
    results_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
