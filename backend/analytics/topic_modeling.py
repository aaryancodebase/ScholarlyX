from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
def discover_topics(documents,n_topics=6,words_per_topic=8):
    docs=[d for d in documents if d.strip()]
    if len(docs)<3: return []
    vectorizer=CountVectorizer(max_df=.95,min_df=1,max_features=5000,stop_words="english")
    matrix=vectorizer.fit_transform(docs)
    if matrix.shape[1]<2: return []
    model=LatentDirichletAllocation(n_components=min(max(2,n_topics),len(docs)),random_state=42,learning_method="batch",max_iter=8)
    model.fit(matrix); terms=vectorizer.get_feature_names_out()
    return [{"topic":i+1,"terms":[terms[j] for j in row.argsort()[-words_per_topic:][::-1]],"weight":round(float(row.sum()),2)} for i,row in enumerate(model.components_)]
