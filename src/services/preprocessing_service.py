import re
import string
import pandas as pd
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class PreprocessingService:
    def __init__(self):
        self.stemmer = StemmerFactory().create_stemmer()
        self.stop_words = set(StopWordRemoverFactory().get_stop_words())

    def preprocess(self, text: str) -> str:
        if text is None or pd.isna(text):
            return ""

        # 1. Cleaning
        text = BeautifulSoup(text, "html.parser").get_text()
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()

        # 2. Casefolding
        
        text = text.lower()

        # 3. Tokenisasi

        tokens = word_tokenize(text)

        # 4. Stopword removal
        # tokens = [w for w in tokens if w not in self.stop_words and len(w) > 2]
        
        filtered_tokens = []

        for w in tokens:
            is_not_stopword = w not in self.stop_words
            is_valid_length = len(w) > 2

            if is_not_stopword and is_valid_length:
                filtered_tokens.append(w)

        tokens = filtered_tokens

        # 5. Stemming
        # tokens = [self.stemmer.stem(w) for w in tokens]
        stemmed_tokens = []

        for w in tokens:
            stemmed_word = self.stemmer.stem(w)
            stemmed_tokens.append(stemmed_word)

        tokens = stemmed_tokens

        return " ".join(tokens)