import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedPrecomputeService:
    def __init__(self, input_csv="dataset/news_preprocess.csv"):
        self.input_csv = input_csv
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2)
        )

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

    def compute_similarity(self, tfidf_csv="dataset/tfidf_matrix.csv", sim_out="dataset/cosine_similarity.csv"):
        tfidf_df = pd.read_csv(tfidf_csv)

        similarity_matrix = cosine_similarity(tfidf_df.values)

        similarity_df = pd.DataFrame(similarity_matrix)
        similarity_df.to_csv(sim_out, index=False)

        return {
            "shape": similarity_df.shape,
            "similarity_out": sim_out
        }