from services.bm25 import rank_bm25
from services.semantic_search import rank_semantic

def rank_hybrid(query,documents,lexical_weight=0.45):
    lexical=dict(rank_bm25(query,documents)); semantic=dict(rank_semantic(query,documents))
    if not documents: return []
    def norm(scores):
        if not scores: return {}
        lo,hi=min(scores.values()),max(scores.values())
        return {k:((v-lo)/(hi-lo) if hi!=lo else 0.0) for k,v in scores.items()}
    a,b=norm(lexical),norm(semantic)
    return sorted([(i,lexical_weight*a.get(i,0)+(1-lexical_weight)*b.get(i,0)) for i in range(len(documents))],key=lambda x:x[1],reverse=True)
