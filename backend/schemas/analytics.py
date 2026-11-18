from pydantic import BaseModel
class AnalyticsOverview(BaseModel):
    total_papers:int
    total_authors:int
    total_searches:int
    average_citations:float
    yearly_publications:list[dict]
    top_categories:list[dict]
