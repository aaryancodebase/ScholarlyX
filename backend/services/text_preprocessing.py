import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer, WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(ENGLISH_STOP_WORDS) - {"no", "nor", "not"}
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
    def clean_text(self, text):
        if not isinstance(text, str): return ""
        text = text.lower()
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"[^a-z0-9+#\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()
    def tokenize(self, text):
        return re.findall(r"[a-z0-9]+(?:[+#]+)?", text)
    def preprocess(self, text):
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        filtered = [t for t in tokens if t not in self.stop_words]
        try: lemmas = [self.lemmatizer.lemmatize(t) for t in filtered]
        except LookupError: lemmas = filtered
        stems = [self.stemmer.stem(t) for t in filtered]
        return {"cleaned_text": cleaned, "tokens": tokens, "filtered_tokens": filtered,
                "lemmatized_tokens": lemmas, "stemmed_tokens": stems,
                "processed_text": " ".join(lemmas), "stemmed_text": " ".join(stems)}
    def process(self, text):
        return self.preprocess(text)["processed_text"]
