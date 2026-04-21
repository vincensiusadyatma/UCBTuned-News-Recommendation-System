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

        max_freq = max(freq.values()) if len(freq) > 0 else 1

        tf = {}
        for word in freq:
            tf[word] = freq[word] / max_freq

        return tf

    def compute_idf(self, documents):
        N = len(documents)
        word_doc_count = {}

        for text in documents:
            words = text.split()
            unique_words = set(words)

            for word in unique_words:
                word_doc_count[word] = word_doc_count.get(word, 0) + 1

        idf = {}
        for word, ni in word_doc_count.items():
            idf[word] = math.log(N / ni)

        return idf


    def compute_tfidf_vector(self, tf_dict, idf_dict):
        tfidf = {}

        for word in tf_dict:
            tfidf[word] = tf_dict[word] * idf_dict.get(word, 0)

        return tfidf


    def cosine_similarity(self, vec1, vec2):
        dot_product = 0

        for word in vec1:
            if word in vec2:
                dot_product += vec1[word] * vec2[word]

        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))

        if norm1 == 0 or norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

    def compute_tfidf(self):
        df = pd.read_csv(self.input_csv)
        df = df.reset_index(drop=True)

       
        df["cbf_text"] = df["Judul"].fillna("") + " " + df["Content"].fillna("")

   
        df["TF"] = df["cbf_text"].apply(self.compute_tf)

        idf = self.compute_idf(df["cbf_text"])

        df["TF_IDF"] = df["TF"].apply(lambda tf: self.compute_tfidf_vector(tf, idf))

        return df


    def compute_similarity(self):
        df = self.compute_tfidf()
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

                rows.append({
                    "news_id": news_list[i].id,
                    "similar_news_id": news_list[j].id,
                    "score": float(sim)
                })

        self.repo.clear_similarity()
        self.repo.insert_similarity(rows)

        return rows

    def recommendation(self, news_id, candidate_size=20):
        df = self.compute_tfidf()
        news_list = self.repo.get_all_news_ordered()

        if len(news_list) != len(df):
            raise ValueError("Jumlah data tidak sama")
        
        news_map = {
            news.id: news.title
            for news in news_list
        }

        target_index = None
        for i, news in enumerate(news_list):
            if news.id == news_id:
                target_index = i
                break

        if target_index is None:
            raise ValueError("News ID tidak ditemukan")

        target_vec = df["TF_IDF"].iloc[target_index]

        results = []

        for i in range(len(df)):
            if i == target_index:
                continue

            sim = self.cosine_similarity(
                target_vec,
                df["TF_IDF"].iloc[i]
            )

            results.append({
                "news_id": news_id,
                "similar_news_id": news_list[i].id,
                "title": news_map.get(news_list[i].id, "Tanpa Judul"),
                "score": float(sim)
            })

       
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        return results[:candidate_size]