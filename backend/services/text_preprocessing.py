
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag


class TextPreprocessor:
    """
    Preprocessing engine for ResearchLens.

    Supports:
    1. Text cleaning
    2. Lowercasing
    3. Tokenization
    4. Stop-word removal
    5. POS-aware lemmatization
    6. Stemming
    """

    def __init__(self):

        # Load English stop words
        self.stop_words = set(stopwords.words("english"))

        # Preserve negation words because they can change meaning
        self.stop_words -= {"no", "nor", "not"}

        # Initialize NLP tools
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()

    # --------------------------------------------------------
    # STEP 1: TEXT CLEANING
    # --------------------------------------------------------

    def clean_text(self, text):

        if not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text
        )

        # Remove HTML tags
        text = re.sub(
            r"<[^>]+>",
            " ",
            text
        )

        # Remove unwanted characters while preserving
        # alphanumeric terms and programming symbols
        text = re.sub(
            r"[^a-z0-9+#\s]",
            " ",
            text
        )

        # Normalize multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # --------------------------------------------------------
    # STEP 2: TOKENIZATION
    # --------------------------------------------------------

    def tokenize(self, text):

        # Preserve terms such as C++, C#, and 3D
        tokens = re.findall(
            r"[a-z0-9]+(?:[+#]+)?",
            text
        )

        return tokens

    # --------------------------------------------------------
    # STEP 3: STOP-WORD REMOVAL
    # --------------------------------------------------------

    def remove_stopwords(self, tokens):

        filtered_tokens = [
            word
            for word in tokens
            if word not in self.stop_words
        ]

        return filtered_tokens

    # --------------------------------------------------------
    # STEP 4: PART-OF-SPEECH MAPPING
    # --------------------------------------------------------

    def get_wordnet_pos(self, tag):

        if tag.startswith("J"):
            return "a"  # Adjective

        elif tag.startswith("V"):
            return "v"  # Verb

        elif tag.startswith("N"):
            return "n"  # Noun

        elif tag.startswith("R"):
            return "r"  # Adverb

        return "n"

    # --------------------------------------------------------
    # STEP 5: LEMMATIZATION
    # --------------------------------------------------------

    def lemmatize(self, tokens):

        tagged_tokens = pos_tag(tokens)

        lemmatized_tokens = []

        for word, tag in tagged_tokens:

            pos = self.get_wordnet_pos(tag)

            lemma = self.lemmatizer.lemmatize(
                word,
                pos=pos
            )

            lemmatized_tokens.append(lemma)

        return lemmatized_tokens

    # --------------------------------------------------------
    # STEP 6: STEMMING
    # --------------------------------------------------------

    def stem(self, tokens):

        stemmed_tokens = [
            self.stemmer.stem(word)
            for word in tokens
        ]

        return stemmed_tokens

    # --------------------------------------------------------
    # COMPLETE PREPROCESSING PIPELINE
    # --------------------------------------------------------

    def preprocess(self, text):

        cleaned_text = self.clean_text(text)

        tokens = self.tokenize(cleaned_text)

        filtered_tokens = self.remove_stopwords(tokens)

        lemmatized_tokens = self.lemmatize(
            filtered_tokens
        )

        stemmed_tokens = self.stem(
            filtered_tokens
        )

        return {
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "filtered_tokens": filtered_tokens,
            "lemmatized_tokens": lemmatized_tokens,
            "stemmed_tokens": stemmed_tokens,
            "processed_text": " ".join(lemmatized_tokens),
            "stemmed_text": " ".join(stemmed_tokens)
        }


# ------------------------------------------------------------
# MANUAL TEST
# ------------------------------------------------------------

if __name__ == "__main__":

    processor = TextPreprocessor()

    sample_text = """
    Researchers are developing advanced machine learning
    models for detecting cyberattacks in computer networks.
    These models were tested using different datasets.
    """

    result = processor.preprocess(sample_text)

    print("\n========== RESEARCHLENS TEXT PREPROCESSING ==========")

    print("\nOriginal Text:")
    print(sample_text)

    print("\nCleaned Text:")
    print(result["cleaned_text"])

    print("\nTokens:")
    print(result["tokens"])

    print("\nAfter Stop-word Removal:")
    print(result["filtered_tokens"])

    print("\nAfter Lemmatization:")
    print(result["lemmatized_tokens"])

    print("\nAfter Stemming:")
    print(result["stemmed_tokens"])

    print("\nFinal Processed Text:")
    print(result["processed_text"])

    print("\n=====================================================")
