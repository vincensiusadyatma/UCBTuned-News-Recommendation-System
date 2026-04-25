from sqlalchemy.orm import Session
from src.repositories.evaluation_repository import EvaluationRepository


class EvaluationService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = EvaluationRepository()

    def precision_at_k(self, recommended, relevant, k):
        rec_k = recommended[:k]
        return len(set(rec_k) & set(relevant)) / k if k > 0 else 0

    def recall_at_k(self, recommended, relevant, k):
        rec_k = recommended[:k]
        return len(set(rec_k) & set(relevant)) / len(relevant) if relevant else 0

    def f1_score(self, p, r):
        return 2 * p * r / (p + r) if (p + r) > 0 else 0

    def average_precision(self, recommended, relevant, k):
        rec_k = recommended[:k]
        score = 0.0
        hit = 0

        for i, item in enumerate(rec_k):
            if item in relevant:
                hit += 1
                score += hit / (i + 1)

        return score / len(relevant) if relevant else 0


    def calculate_mean_metrics(self, evaluation_data: list[dict]):
        if not evaluation_data:
            return {
                "precision": 0,
                "recall": 0,
                "f1_score": 0,
                "map": 0
            }

        n = len(evaluation_data)

        mean_precision = sum(d["precision"] for d in evaluation_data) / n
        mean_recall = sum(d["recall"] for d in evaluation_data) / n
        mean_f1 = sum(d["f1_score"] or 0 for d in evaluation_data) / n
        mean_map = sum(d["map_score"] or 0 for d in evaluation_data) / n

        return {
            "precision": mean_precision,
            "recall": mean_recall,
            "f1_score": mean_f1,
            "map": mean_map
        }