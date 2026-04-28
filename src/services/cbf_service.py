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

        if len(freq) > 0:
            max_freq = max(freq.values())
        else:
            max_freq = 1

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
                if word in word_doc_count:
                    word_doc_count[word] += 1
                else:
                    word_doc_count[word] = 1

        idf = {}

        for word in word_doc_count:
            ni = word_doc_count[word]
            idf[word] = math.log(N / ni)

        return idf

    def compute_tfidf_vector(self, tf_dict, idf_dict):
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
                dot_product += vec1[word] * vec2[word]

        sum1 = 0
        for v in vec1.values():
            sum1 += v * v
        norm1 = math.sqrt(sum1)

        sum2 = 0
        for v in vec2.values():
            sum2 += v * v
        norm2 = math.sqrt(sum2)

     
        if norm1 == 0:
            return 0
        if norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

 
    def compute_tfidf(self):
        df = pd.read_csv(self.input_csv)

   
        df = df.reset_index(drop=True)

   
        df["cbf_text"] = df["Judul"].fillna("") + " " + df["Content"].fillna("")

        tf_list = []
        for text in df["cbf_text"]:
            tf = self.compute_tf(text)
            tf_list.append(tf)

        df["TF"] = tf_list

 
        idf = self.compute_idf(df["cbf_text"])

     
        tfidf_list = []
        for tf in df["TF"]:
            tfidf = self.compute_tfidf_vector(tf, idf)
            tfidf_list.append(tfidf)

        df["TF_IDF"] = tfidf_list

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

                vec1 = df["TF_IDF"].iloc[i]
                vec2 = df["TF_IDF"].iloc[j]

                sim = self.cosine_similarity(vec1, vec2)

                row = {
                    "news_id": news_list[i].id,
                    "similar_news_id": news_list[j].id,
                    "score": float(sim)
                }

                rows.append(row)

        self.repo.clear_similarity()
        self.repo.insert_similarity(rows)

        return rows


    def recommendation(self, news_id, candidate_size=20):
        df = self.compute_tfidf()
        news_list = self.repo.get_all_news_ordered()

        if len(news_list) != len(df):
            raise ValueError("Jumlah data tidak sama")

  
        news_map = {}
        for news in news_list:
            news_map[news.id] = news.title

        target_index = None
        for i in range(len(news_list)):
            if news_list[i].id == news_id:
                target_index = i
                break

        if target_index is None:
            raise ValueError("News ID tidak ditemukan")

        target_vec = df["TF_IDF"].iloc[target_index]

        results = []

        for i in range(len(df)):

            if i == target_index:
                continue

            vec = df["TF_IDF"].iloc[i]
            sim = self.cosine_similarity(target_vec, vec)

            result = {
                "news_id": news_id,
                "similar_news_id": news_list[i].id,
                "title": news_map.get(news_list[i].id, "Tanpa Judul"),
                "score": float(sim)
            }

            results.append(result)

      
        results = sorted(results, key=lambda item: item["score"], reverse=True)

        return results[:candidate_size]