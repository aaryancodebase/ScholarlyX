import os
from fastapi import APIRouter,HTTPException
from ingestion.importer import import_papers
router=APIRouter(prefix="/api/v1/admin",tags=["Administration"])
@router.post("/import")
def import_dataset(limit:int|None=None):
    target=limit or int(os.getenv("DATASET_SIZE","1000"))
    if target<1 or target>10000:raise HTTPException(status_code=400,detail="limit must be between 1 and 10000")
    try:return import_papers(target)
    except Exception as exc:raise HTTPException(status_code=502,detail=f"Dataset import failed: {exc}")
