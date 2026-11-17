
import os
import requests

from pathlib import Path
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

# Load environment variables from backend/.env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BASE_URL = "https://api.openalex.org/works"

API_KEY = os.getenv("OPENALEX_API_KEY", "").strip()

# Fields required for ResearchLens
SELECT_FIELDS = ",".join([
    "id",
    "doi",
    "title",
    "publication_year",
    "authorships",
    "abstract_inverted_index",
    "primary_topic",
    "cited_by_count",
    "open_access",
    "type"
])


# ============================================================
# ABSTRACT RECONSTRUCTION
# ============================================================

def reconstruct_abstract(inverted_index):
    """
    Convert OpenAlex's inverted abstract index
    into normal readable text.
    """

    if not inverted_index:
        return None

    words = {}

    for word, positions in inverted_index.items():
        for position in positions:
            words[position] = word

    if not words:
        return None

    return " ".join(
        words[position]
        for position in sorted(words)
    )


# ============================================================
# OPENALEX DATA COLLECTION
# ============================================================

def fetch_papers(limit=10):
    """
    Fetch Computer Science research papers
    from the OpenAlex API.

    Parameters:
        limit (int): Number of papers to collect.

    Returns:
        list: Research paper records with reconstructed abstracts.
    """

    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit must be a positive integer")

    papers = []
    page = 1

    # Corrected OpenAlex filter
    params = {
        "filter": (
            "primary_topic.field.id:17,"
            "has_abstract:true,"
            "publication_year:2018-2026,"
            "type:article"
        ),

        "per_page": min(limit, 100),
        "page": page,
        "select": SELECT_FIELDS
    }

    # API key is optional
    if API_KEY:
        params["api_key"] = API_KEY

    session = requests.Session()

    session.headers.update({
        "User-Agent": "ResearchLens/1.0"
    })

    try:

        while len(papers) < limit:

            params["page"] = page

            print(f"\nRequesting OpenAlex page {page}...")

            response = session.get(
                BASE_URL,
                params=params,
                timeout=30
            )

            # Improved API error reporting
            if response.status_code != 200:

                print("\nOpenAlex API Error!")
                print("Status code:", response.status_code)
                print("Error details:", response.text)

                response.raise_for_status()

            data = response.json()

            results = data.get("results", [])

            if not results:
                print("No more research papers available.")
                break

            for item in results:

                # Reconstruct abstract
                abstract = reconstruct_abstract(
                    item.get("abstract_inverted_index")
                )

                # Skip incomplete records
                if not item.get("title") or not abstract:
                    continue

                item["abstract"] = abstract

                papers.append(item)

                if len(papers) >= limit:
                    break

            print(
                f"Collected {len(papers)}/{limit} papers"
            )

            page += 1

        return papers

    finally:
        session.close()


# ============================================================
# TESTING AND DATA PREVIEW
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("RESEARCHLENS - OPENALEX DATA COLLECTION")
    print("=" * 55)

    try:

        results = fetch_papers(limit=10)

        print("\n========== DATASET PREVIEW ==========")

        for index, paper in enumerate(results, start=1):

            print(f"\nPaper {index}")

            print("Title:", paper.get("title"))

            print("Year:", paper.get("publication_year"))

            print("DOI:", paper.get("doi"))

            print("Type:", paper.get("type"))

            print(
                "Abstract:",
                paper["abstract"][:250],
                "..."
            )

            authorships = paper.get("authorships", [])

            print("Authors:", len(authorships))

            topic = paper.get("primary_topic") or {}

            print(
                "Primary topic:",
                topic.get("display_name")
            )

        print("\n" + "=" * 55)
        print("DATA COLLECTION COMPLETED")
        print("Total papers collected:", len(results))
        print("=" * 55)

    except requests.RequestException as error:

        print("\nNetwork/API request failed:")
        print(error)

    except Exception as error:

        print("\nUnexpected error occurred:")
        print(error)
