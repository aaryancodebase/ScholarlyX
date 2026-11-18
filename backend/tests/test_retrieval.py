from services.bm25 import rank_bm25
from services.tfidf import rank_tfidf
from services.boolean_retrieval import boolean_search
from evaluation.metrics import precision_at_k,recall_at_k,ndcg_at_k
DOCS=["neural network deep learning","database query optimization","neural information retrieval"]
def test_bm25():assert rank_bm25("neural network",DOCS)[0][0]==0
def test_tfidf():assert rank_tfidf("database optimization",DOCS)[0][0]==1
def test_boolean_and():assert boolean_search("neural AND learning",DOCS)==[0]
def test_boolean_or_not():assert boolean_search("(database OR neural) AND NOT learning",DOCS)==[1,2]
def test_metrics():
    rel={"a","b"};got=["a","c","b"]
    assert precision_at_k(rel,got,2)==.5 and recall_at_k(rel,got,2)==.5
    assert 0<ndcg_at_k(rel,got,3)<=1
