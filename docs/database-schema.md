# Database schema
The six existing tables are preserved.
- papers: source ID, title, abstract, year, DOI, URL, citation count, category, created timestamp.
- authors: external OpenAlex ID and name.
- paper_authors: many-to-many paper/author association with author position.
- topics: topic name, description and model version.
- paper_topics: paper/topic association with confidence.
- search_queries: query text, retrieval method, result count and timestamp.
UUID primary keys and foreign-key association tables are used.
