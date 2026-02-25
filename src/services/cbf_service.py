import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.repositories import CbfRepository


class CbfService:
    def __init__(self, input_csv="dataset/news_preprocess.csv"):
        self.input_csv = input_csv
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2)
        )

        self.repo = CbfRepository()

    def compute_tfidf(self, tfidf_out="dataset/tfidf_matrix.csv"):
        df = pd.read_csv(self.input_csv)

        df["cbf_text"] = df["Judul"].fillna("") + " " + df["Content"].fillna("")

        tfidf_matrix = self.vectorizer.fit_transform(df["cbf_text"])

        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=self.vectorizer.get_feature_names_out()
        )

        tfidf_df.to_csv(tfidf_out, index=False)

        return {
            "rows": len(df),
            "shape": tfidf_df.shape,
            "tfidf_out": tfidf_out
        }

    def compute_similarity(self, tfidf_csv="dataset/tfidf_matrix.csv", export_csv="dataset/news_similarity_topk.csv", top_k=5):
        tfidf_df = pd.read_csv(tfidf_csv)
        similarity_matrix = cosine_similarity(tfidf_df.values)

        news_list = self.repo.get_all_news_ordered()

        rows_to_insert = []
        rows_to_export = []

        for i, news in enumerate(news_list):
            scores = similarity_matrix[i]

            ranked_indices = scores.argsort()[::-1]
            ranked_indices = [idx for idx in ranked_indices if idx != i][:top_k]

            for j in ranked_indices:
                rows_to_insert.append({
                    "news_id": news.id,
                    "similar_news_id": news_list[j].id,
                    "score": float(scores[j])
                })

                rows_to_export.append({
                    "news_id": news.id,
                    "similar_news_id": news_list[j].id,
                    "score": float(scores[j])
                })

        self.repo.clear_similarity()
        self.repo.insert_similarity(rows_to_insert)

        pd.DataFrame(rows_to_export).to_csv(export_csv, index=False)
        return {
            "rows_inserted": len(rows_to_insert),
            "export_csv": export_csv,
            "top_k": top_k
        }

    def recomendation(self, news_id: int, top_k: int = 5):
        try:
            similarities = self.repo.get_top_similar_news(news_id, top_k)

            results = []
            for sim in similarities:
                results.append({
                    "news_id": sim.similar_news.id,
                    "title": sim.similar_news.title,
                    # "content": sim.similar_news.content,
                    "score": float(sim.score),
                })

            return results
        finally:
            print("selesai")
        
