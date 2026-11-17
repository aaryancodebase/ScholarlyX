
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models import Paper, Author, paper_authors

from ingestion.openalex import fetch_papers


# ============================================================
# AUTHOR MANAGEMENT
# ============================================================

def get_or_create_author(
    db: Session,
    author_data: dict,
    cache: dict
):
    """
    Find an existing author or create a new one.
    Uses caching to avoid repeated database queries.
    """

    author_id = author_data.get("id")
    author_name = author_data.get("display_name")

    if not author_name:
        return None

    author_name = author_name.strip()

    # Generate a unique cache key
    cache_key = (
        author_id
        if author_id
        else author_name.casefold()
    )

    # Check local cache first
    if cache_key in cache:
        return cache[cache_key]

    author = None

    # Search using OpenAlex ID
    if author_id:
        author = (
            db.query(Author)
            .filter(Author.external_id == author_id)
            .first()
        )

    # Fallback when external ID is unavailable
    else:
        author = (
            db.query(Author)
            .filter(Author.name == author_name)
            .first()
        )

    # Create author if not found
    if author is None:

        author = Author(
            external_id=author_id,
            name=author_name
        )

        db.add(author)
        db.flush()

    # Store in cache
    cache[cache_key] = author

    return author


# ============================================================
# PAPER IMPORTER
# ============================================================

def import_papers(limit=100):
    """
    Fetch research papers from OpenAlex
    and store them in PostgreSQL.
    """

    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit must be a positive integer")

    db = SessionLocal()

    inserted = 0
    skipped = 0
    authors_linked = 0
    duplicate_authors_skipped = 0

    # Cache authors during the import
    author_cache = {}

    try:

        print("\n" + "=" * 55)
        print("RESEARCHLENS DATA INGESTION")
        print("=" * 55)

        print(f"Target paper count: {limit}")

        # ----------------------------------------------------
        # STEP 1: FETCH PAPERS
        # ----------------------------------------------------

        papers = fetch_papers(limit=limit)

        print(f"\nFetched {len(papers)} papers from OpenAlex.")

        # ----------------------------------------------------
        # STEP 2: PROCESS EACH PAPER
        # ----------------------------------------------------

        for item in papers:

            source_id = item.get("id")
            title = item.get("title")
            abstract = item.get("abstract")

            # Validate essential metadata
            if not source_id or not title or not abstract:
                skipped += 1
                continue

            # ------------------------------------------------
            # STEP 3: CHECK DUPLICATE PAPERS
            # ------------------------------------------------

            existing = (
                db.query(Paper)
                .filter(Paper.source_id == source_id)
                .first()
            )

            if existing:
                skipped += 1
                continue

            # Check duplicate DOI
            doi = item.get("doi")

            if doi:

                existing_doi = (
                    db.query(Paper)
                    .filter(Paper.doi == doi)
                    .first()
                )

                if existing_doi:
                    skipped += 1
                    continue

            # ------------------------------------------------
            # STEP 4: EXTRACT PAPER METADATA
            # ------------------------------------------------

            primary_topic = item.get("primary_topic") or {}

            subfield = primary_topic.get("subfield") or {}

            open_access = item.get("open_access") or {}

            paper = Paper(
                source_id=source_id,
                title=title,
                abstract=abstract,
                publication_year=item.get("publication_year"),
                doi=doi,
                paper_url=open_access.get("oa_url"),
                citation_count=item.get("cited_by_count") or 0,
                category=subfield.get("display_name")
            )

            db.add(paper)

            # Flush generates the paper UUID
            db.flush()

            # ------------------------------------------------
            # STEP 5: EXTRACT AND LINK AUTHORS
            # ------------------------------------------------

            authorships = item.get("authorships") or []

            # Prevent duplicate relationships for this paper
            seen_author_ids = set()

            for position, authorship in enumerate(authorships):

                author_data = authorship.get("author") or {}

                author = get_or_create_author(
                    db,
                    author_data,
                    author_cache
                )

                if author is None:
                    continue

                # Critical fix:
                # The same author cannot be linked twice
                # to the same paper.
                if author.id in seen_author_ids:

                    duplicate_authors_skipped += 1
                    continue

                seen_author_ids.add(author.id)

                # Insert paper-author relationship
                db.execute(
                    paper_authors.insert().values(
                        paper_id=paper.id,
                        author_id=author.id,
                        author_position=position
                    )
                )

                authors_linked += 1

            inserted += 1

            print(
                f"Imported {inserted}/{len(papers)}: "
                f"{title[:65]}"
            )

        # ----------------------------------------------------
        # STEP 6: COMMIT TRANSACTION
        # ----------------------------------------------------

        db.commit()

        print("\n" + "=" * 55)
        print("RESEARCHLENS INGESTION COMPLETED")
        print("=" * 55)

        print(f"New papers inserted       : {inserted}")
        print(f"Duplicate/invalid papers  : {skipped}")
        print(f"Author relationships      : {authors_linked}")
        print(f"Duplicate author links    : {duplicate_authors_skipped}")

        print("=" * 55)

    except Exception as error:

        # Roll back all uncommitted changes
        db.rollback()

        print("\nINGESTION FAILED")
        print("Database transaction rolled back.")
        print("Error:", error)

        raise

    finally:

        # Always release database session
        db.close()


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":

    import_papers(limit=100)
