import pandas as pd
import math
from collections import Counter
from src.repositories import CbfRepository


class CbfService:
    def __init__(self, input_csv="dataset/news_preprocess.csv"):
        self.input_csv = input_csv
        self.repo = CbfRepository()

    def compute_tf(self, text):
        words = text.split()
        freq = Counter(words)

        # cari max frequency
        if len(freq) == 0:
            max_freq = 1
        else:
            max_freq = max(freq.values())

        tf = {}

        for word in freq:
            count = freq[word]
            tf[word] = count / max_freq

        return tf

 
    def compute_idf(self, documents):
        N = len(documents)
        word_doc_count = {}

        for text in documents:
            words = text.split()
            unique_words = set(words)

            for word in unique_words:
                if word in word_doc_count:
                    word_doc_count[word] = word_doc_count[word] + 1
                else:
                    word_doc_count[word] = 1

        idf = {}

        for word in word_doc_count:
            ni = word_doc_count[word]
            idf[word] = math.log(N / ni)

        return idf


    def compute_tfidf(self, tf_dict, idf_dict):
        tfidf = {}

        for word in tf_dict:
            if word in idf_dict:
                tfidf[word] = tf_dict[word] * idf_dict[word]
            else:
                tfidf[word] = 0

        return tfidf


    def cosine_similarity(self, vec1, vec2):
        dot_product = 0

        for word in vec1:
            if word in vec2:
                dot_product = dot_product + (vec1[word] * vec2[word])

        norm1 = 0
        for value in vec1.values():
            norm1 = norm1 + (value * value)
        norm1 = math.sqrt(norm1)

        norm2 = 0
        for value in vec2.values():
            norm2 = norm2 + (value * value)
        norm2 = math.sqrt(norm2)

        if norm1 == 0:
            return 0

        if norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

 
    def compute_tfidf_manual(self):
        df = pd.read_csv(self.input_csv)
        df = df.reset_index(drop=True)

        df["cbf_text"] = df["Judul"].fillna("") + " " + df["Content"].fillna("")

        # TF
        tf_list = []
        for text in df["cbf_text"]:
            tf_list.append(self.compute_tf(text))
        df["TF"] = tf_list

        # IDF
        idf = self.compute_idf(df["cbf_text"])

        # TF-IDF
        tfidf_list = []
        for tf in df["TF"]:
            tfidf_list.append(self.compute_tfidf(tf, idf))
        df["TF_IDF"] = tfidf_list

        return df

 
    def compute_similarity(self):
        df = self.compute_tfidf_manual()
        news_list = self.repo.get_all_news_ordered()

        if len(news_list) != len(df):
            raise ValueError("Jumlah data tidak sama")

        rows = []

        for i in range(len(df)):
            for j in range(len(df)):

                if i == j:
                    continue

                sim = self.cosine_similarity(
                    df["TF_IDF"].iloc[i],
                    df["TF_IDF"].iloc[j]
                )

                data = {}
                data["news_id"] = news_list[i].id
                data["similar_news_id"] = news_list[j].id
                data["score"] = float(sim)

                rows.append(data)

        self.repo.clear_similarity()
        self.repo.insert_similarity(rows)

        return rows