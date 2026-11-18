from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"backend"))
from evaluation.metrics import precision_at_k,recall_at_k,average_precision,ndcg_at_k
# Demonstration only: replace IDs with a human-judged relevance set before reporting metrics.
relevant={"paper-A","paper-C"}; retrieved=["paper-A","paper-B","paper-C","paper-D"]
print({"precision@3":precision_at_k(relevant,retrieved,3),"recall@3":recall_at_k(relevant,retrieved,3),"MAP":average_precision(relevant,retrieved),"NDCG@3":ndcg_at_k(relevant,retrieved,3)})
