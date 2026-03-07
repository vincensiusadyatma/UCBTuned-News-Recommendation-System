import math
from src.repositories import UcbTunedRepository
from src.services.cbf_service import CbfService


class UcbTunedService:
    def __init__(self):
        self.ucb_repo = UcbTunedRepository()
        self.cbf_service = CbfService()

    def _mean_reward(self, rewards: list[int]) -> float:
        if not rewards:
            return 0.0
        return sum(rewards) / len(rewards)

    def _variance_vj(self, rewards: list[int], t: int) -> float:
        s = len(rewards)
        if s == 0:
            return 0.0

        t = max(t, 2)  

        mean = self._mean_reward(rewards)
        mean_square = sum(x**2 for x in rewards) / s

        return (
            mean_square
            - (mean ** 2)
            + math.sqrt((2 * math.log(t)) / s)
        )

 
    def _ucb_tuned_score(self, rewards: list[int], t: int) -> float:
        s = len(rewards)
        if s == 0:
            return 0.0 

        t = max(t, 2)

        mean = self._mean_reward(rewards)
        vj = self._variance_vj(rewards, t)

        bonus = math.sqrt(
            (2 * math.log(t) / s) * min(0.25, vj)
        )

        return mean + bonus

    def recommend(self, news_id: int, top_k: int = 5):
        cbf_candidates = self.cbf_service.recomendation(news_id, top_k=top_k)

        if not cbf_candidates:
            return []

        candidate_ids = [item["news_id"] for item in cbf_candidates]
        feedback_stats = self.ucb_repo.get_feedback_by_news_ids(candidate_ids)

        t = sum(len(v.get("rewards", [])) for v in feedback_stats.values())
        t = max(t, 2)

        ranked = []
        for item in cbf_candidates:
            nid = item["news_id"]
            rewards = feedback_stats.get(nid, {}).get("rewards", [])

            mean = self._mean_reward(rewards)
            vj = self._variance_vj(rewards, t)
            ucb_score = self._ucb_tuned_score(rewards, t)

            ranked.append({
                "news_id": nid,
                "title": item["title"],
                "cbf_score": float(item["score"]),
                "ucb_score": float(ucb_score),
                "mean_reward": float(mean),
                "views": len(rewards),
                "clicks": sum(rewards),
                "V_j": float(vj)
            })

        ranked.sort(key=lambda x: x["ucb_score"], reverse=True)
        return ranked

    def close(self):
        self.ucb_repo.close()