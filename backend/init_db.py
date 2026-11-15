
from core.database import engine, Base

from models import Paper, Author, Topic, SearchQuery

def initialize_database():
    print("Initializing ResearchLens database...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    initialize_database()
