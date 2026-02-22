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

        text = text.lower()
        text = BeautifulSoup(text, "html.parser").get_text()
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()

        tokens = word_tokenize(text)
        tokens = [w for w in tokens if w not in self.stop_words and len(w) > 2]
        tokens = [self.stemmer.stem(w) for w in tokens]

        return " ".join(tokens)
    