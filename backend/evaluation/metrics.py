import math
def precision_at_k(relevant,retrieved,k):
    return sum(x in relevant for x in retrieved[:k])/k if k>0 else 0.0
def recall_at_k(relevant,retrieved,k):
    return sum(x in relevant for x in retrieved[:k])/len(relevant) if relevant else 0.0
def average_precision(relevant,retrieved):
    if not relevant:return 0.0
    hits=total=0
    for rank,item in enumerate(retrieved,1):
        if item in relevant:
            hits+=1; total+=hits/rank
    return total/len(relevant)
def ndcg_at_k(relevant,retrieved,k):
    def dcg(items):
        return sum(1/math.log2(i+2) for i,item in enumerate(items[:k]) if item in relevant)
    ideal=dcg(list(relevant))
    return dcg(retrieved)/ideal if ideal else 0.0
