from core.database import engine,Base
import models
if __name__=="__main__":
    print("Initializing ResearchLens database (existing tables are preserved)...")
    Base.metadata.create_all(bind=engine)
    print("Database tables are ready.")
