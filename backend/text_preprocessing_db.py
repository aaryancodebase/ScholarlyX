
from core.database import SessionLocal
from models import Paper

from services.text_preprocessing import TextPreprocessor


def test_database_preprocessing():

    db = SessionLocal()

    try:

        # Fetch one research paper
        paper = db.query(Paper).filter(
            Paper.abstract.isnot(None)
        ).first()

        if paper is None:
            print("No research paper abstracts found.")
            return

        processor = TextPreprocessor()

        result = processor.preprocess(paper.abstract)

        print("\n========== DATABASE PREPROCESSING ==========")

        print("\nPaper Title:")
        print(paper.title)

        print("\nOriginal Abstract:")
        print(paper.abstract[:500])

        print("\nProcessed Abstract:")
        print(result["processed_text"][:500])

        print("\nOriginal Token Count:")
        print(len(result["tokens"]))

        print("\nAfter Stop-word Removal:")
        print(len(result["filtered_tokens"]))

        print("\nAfter Lemmatization:")
        print(len(result["lemmatized_tokens"]))

        print("\n============================================")

    finally:
        db.close()


if __name__ == "__main__":
    test_database_preprocessing()
