from fastapi import APIRouter
from pydantic import BaseModel,Field
from evaluation.metrics import precision_at_k,recall_at_k,average_precision,ndcg_at_k
router=APIRouter(prefix="/api/v1/evaluation",tags=["Evaluation"])
class EvaluationRequest(BaseModel):
    relevant_ids:list[str]=Field(min_length=1)
    retrieved_ids:list[str]=Field(min_length=1)
    k:int=Field(default=10,ge=1,le=100)
@router.post("/metrics")
def evaluate(payload:EvaluationRequest):
    relevant=set(payload.relevant_ids);retrieved=payload.retrieved_ids
    return {"k":payload.k,"precision_at_k":round(precision_at_k(relevant,retrieved,payload.k),4),
        "recall_at_k":round(recall_at_k(relevant,retrieved,payload.k),4),
        "map":round(average_precision(relevant,retrieved),4),
        "ndcg_at_k":round(ndcg_at_k(relevant,retrieved,payload.k),4),
        "note":"Metrics are meaningful only when relevant_ids are human-judged relevance labels."}
