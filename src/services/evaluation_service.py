from sqlalchemy.orm import Session
from collections import defaultdict
from src.repositories.evaluation_repository import EvaluationRepository


class EvaluationService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = EvaluationRepository(db)

  
    def precision_at_k(self, recommended, relevant, k):

        recommended_at_k = recommended[:k]

        relevant_items = (
            set(recommended_at_k) & set(relevant)
        )

        total_relevant_items = len(relevant_items)

        if k > 0:
            precision = total_relevant_items / k
        else:
            precision = 0

        return precision

    def recall_at_k(self, recommended, relevant, k):
        recommended_at_k = recommended[:k]
        relevant_set = set(relevant)

        relevant_items = set(recommended_at_k) & relevant_set

        if len(relevant_set) > 0:
            recall = len(relevant_items) / len(relevant_set)
        else:
            recall = 0

        return recall
    
    def f1_score(self, precision, recall):

        if (precision + recall) > 0:

            f1 = (
                2 * precision * recall / (precision + recall)
            )

        else:
            f1 = 0

        return f1
    
    def average_precision(self, recommended, relevant, k):
        recommended_at_k = recommended[:k]

        total_score = 0.0
        total_hit = 0
        relevant_set = set(relevant)

        for index, item in enumerate(recommended_at_k):
            if item in relevant_set:
                total_hit += 1
                precision = total_hit / (index + 1)
                total_score += precision

        if len(relevant_set) > 0:
            average_precision = total_score / min(len(relevant_set), k)
        else:
            average_precision = 0

        return average_precision


    def calculate_map(self, evaluation_data):
        if not evaluation_data:
            return 0

        user_ap = defaultdict(list)

        for data in evaluation_data:
            user_id = data["user_id"]
            average_precision = (
                data.get("average_precision", 0)
                or 0
            )
            user_ap[user_id].append(
                average_precision
            )

        mean_per_user = []

        for ap_list in user_ap.values():
            mean_average_precision = (
                sum(ap_list) /
                len(ap_list)
            )
            mean_per_user.append(
                mean_average_precision
            )

        if len(mean_per_user) > 0:
            map_score = (
                sum(mean_per_user) /
                len(mean_per_user)
            )

        else:
            map_score = 0

        return map_score


    def calculate_mean_metrics(self, evaluation_data: list[dict]):
        if not evaluation_data:
            return {
                "precision": 0,
                "recall": 0,
                "f1_score": 0,
                "map": 0
            }

        n = len(evaluation_data)

        return {
            "precision": sum(d["precision"] for d in evaluation_data) / n,
            "recall": sum(d["recall"] for d in evaluation_data) / n,
            "f1_score": sum(d["f1_score"] for d in evaluation_data) / n,
            "map": self.calculate_map(evaluation_data) 
        }
    
    def get_metric_by_user_id(self, user_id: int):
        results = self.repo.get_all()

        user_results = [r for r in results if r.user_id == user_id]

        if not user_results:
            return None

        data = {
            "user_id": user_id,
            "precision": {},
            "recall": {},
            "f1_score": {},
            "average_precision": {}
        }

        for r in user_results:
            k_key = f"k{r.k}"

            data["precision"][k_key] = r.precision
            data["recall"][k_key] = r.recall
            data["f1_score"][k_key] = r.f1_score
            data["average_precision"][k_key] = r.average_precision or 0

        return data
    
    def get_general_metrics(self, metric_name: str):
        results = self.repo.get_all()

        if not results:
            return {}

        grouped = defaultdict(list)

        for r in results:
            k_key = f"k{r.k}"

            value = getattr(r, metric_name, 0) or 0

            grouped[k_key].append(value)

        return {
            k: round(sum(values) / len(values), 6)
            for k, values in grouped.items()
        }