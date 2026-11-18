import re
from collections import Counter
def extractive_summary(text,max_sentences=3):
    if not text: return ""
    sentences=[s.strip() for s in re.split(r"(?<=[.!?])\\s+",text) if len(s.strip())>30]
    if len(sentences)<=max_sentences: return " ".join(sentences)
    freq=Counter(re.findall(r"[a-zA-Z]{3,}",text.lower()))
    scored=[]
    for i,s in enumerate(sentences):
        terms=re.findall(r"[a-zA-Z]{3,}",s.lower())
        scored.append((sum(freq[t] for t in terms)/max(len(terms),1),i,s))
    return " ".join(x[2] for x in sorted(sorted(scored,reverse=True)[:max_sentences],key=lambda x:x[1]))
