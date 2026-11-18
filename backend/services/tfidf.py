from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_tfidf(query, documents):
    if not documents: return []
    vectorizer=TfidfVectorizer(ngram_range=(1,2),max_features=50000)
    matrix=vectorizer.fit_transform(documents+[query])
    scores=cosine_similarity(matrix[-1],matrix[:-1]).ravel()
    return sorted(enumerate(scores.tolist()),key=lambda x:x[1],reverse=True)
