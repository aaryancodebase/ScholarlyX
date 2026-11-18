import math
from collections import Counter

def rank_bm25(query, documents, k1=1.5, b=0.75):
    tokenized=[d.split() for d in documents]
    if not tokenized: return []
    n=len(tokenized); avgdl=sum(map(len,tokenized))/max(n,1); df=Counter()
    for doc in tokenized: df.update(set(doc))
    qterms=set(query.split()); ranked=[]
    for i,doc in enumerate(tokenized):
        counts=Counter(doc); dl=len(doc); score=0.0
        for term in qterms:
            freq=counts[term]
            if not freq: continue
            idf=math.log(1+(n-df[term]+0.5)/(df[term]+0.5))
            score+=idf*(freq*(k1+1))/(freq+k1*(1-b+b*dl/max(avgdl,1)))
        ranked.append((i,score))
    return sorted(ranked,key=lambda x:x[1],reverse=True)
