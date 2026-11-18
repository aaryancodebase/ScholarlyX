from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
def cluster_documents(documents,n_clusters=5):
    if len(documents)<3: return []
    vectorizer=TfidfVectorizer(max_features=8000,stop_words="english")
    matrix=vectorizer.fit_transform(documents)
    k=min(max(2,n_clusters),len(documents))
    model=KMeans(n_clusters=k,random_state=42,n_init=10); labels=model.fit_predict(matrix)
    terms=vectorizer.get_feature_names_out(); result=[]
    for cid in range(k):
        center=model.cluster_centers_[cid]
        result.append({"cluster":cid,"count":int((labels==cid).sum()),"keywords":[terms[i] for i in center.argsort()[-6:][::-1]]})
    return result
