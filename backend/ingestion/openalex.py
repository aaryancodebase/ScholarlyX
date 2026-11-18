import os,time,requests
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/".env")
BASE_URL="https://api.openalex.org/works"
API_KEY=os.getenv("OPENALEX_API_KEY","").strip()
SELECT_FIELDS="id,doi,title,publication_year,authorships,abstract_inverted_index,primary_topic,cited_by_count,open_access,type"
def reconstruct_abstract(index):
    if not index:return None
    words={}
    for word,positions in index.items():
        for pos in positions:words[pos]=word
    return " ".join(words[i] for i in sorted(words)) if words else None
def fetch_papers(limit=100):
    if not isinstance(limit,int) or limit<=0:raise ValueError("limit must be positive")
    collected=[];params={"filter":"primary_topic.field.id:17,has_abstract:true,publication_year:2018-2026,type:article","per-page":min(limit,100),"select":SELECT_FIELDS,"cursor":"*"}
    if API_KEY:params["api_key"]=API_KEY
    with requests.Session() as session:
        while len(collected)<limit:
            response=session.get(BASE_URL,params=params,headers={"User-Agent":"ResearchLens/2.0 academic project"},timeout=45)
            response.raise_for_status();payload=response.json()
            for item in payload.get("results",[]):
                abstract=reconstruct_abstract(item.get("abstract_inverted_index"))
                if item.get("title") and abstract:
                    item["abstract"]=abstract;collected.append(item)
                if len(collected)>=limit:break
            cursor=payload.get("meta",{}).get("next_cursor")
            if not cursor:break
            params["cursor"]=cursor;time.sleep(.15)
    return collected
if __name__=="__main__":
    rows=fetch_papers(10)
    for i,p in enumerate(rows,1):print(f"{i}. {p['title']} ({p.get('publication_year')})")
    print("Collected:",len(rows))
