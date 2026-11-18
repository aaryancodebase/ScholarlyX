from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from core.database import engine
from api.search import router as search_router
from api.papers import router as papers_router
from api.analytics import router as analytics_router
from api.admin import router as admin_router
from api.evaluation import router as evaluation_router
app=FastAPI(title="ScholarlyX API",description="Hybrid academic research retrieval and text analytics platform",version="2.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(search_router);app.include_router(papers_router);app.include_router(analytics_router);app.include_router(admin_router);app.include_router(evaluation_router)
@app.get("/")
def root():return {"name":"ScholarlyX API","status":"running","docs":"/docs"}
@app.get("/api/v1/health")
def health():
    try:
        with engine.connect() as conn:conn.execute(text("SELECT 1"))
        return {"status":"healthy","database":"connected"}
    except Exception as exc:return {"status":"unhealthy","database":"disconnected","error":str(exc)}
