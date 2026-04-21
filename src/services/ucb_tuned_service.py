import math
from src.repositories import UcbTunedRepository
from src.services.cbf_service import CbfService


class UcbTunedService:
    def __init__(self):
        self.ucb_repo = UcbTunedRepository()
        self.cbf_service = CbfService()


    def _mean_reward(self, rewards):
        if not rewards:
            return 0.0
        return sum(rewards) / len(rewards)

  
    def _variance_vj(self, rewards, t):
        s = len(rewards)

        if s == 0:
            return 0.0

        t = max(t, 2)

        mean = self._mean_reward(rewards)
        mean_square = sum(x**2 for x in rewards) / s

        return mean_square - (mean ** 2) + math.sqrt((2 * math.log(t)) / s)


    def _ucb_tuned_score(self, rewards, t):
        s = len(rewards)

        if s == 0:
            return 0.0  

        t = max(t, 2)

        mean = self._mean_reward(rewards)
        vj = self._variance_vj(rewards, t)

        bonus = math.sqrt((math.log(t) / s) * min(0.25, vj))

        return mean + bonus

    def recommend(self, news_id, top_k=5, candidate_size=20):
        candidate_size = max(candidate_size, top_k)

        cbf_candidates = self.cbf_service.recommendation(
            news_id,
            candidate_size=candidate_size
        )

        if not cbf_candidates:
            return {
                "recommendations": [],
                "all_ranked": []
            }

        candidate_ids = [item["similar_news_id"] for item in cbf_candidates]

        feedback_stats = self.ucb_repo.get_feedback_by_news_ids(candidate_ids)

        # total interaksi global
        t = sum(len(v.get("rewards", [])) for v in feedback_stats.values())
        t = max(t, 2)

        ranked = []

        for item in cbf_candidates:
            nid = item["similar_news_id"]
            raw_rewards = feedback_stats.get(nid, {}).get("rewards", [])
            s = len(raw_rewards)

            title = item.get("title", "")

       
            if s == 0:
                ranked.append({
                    "news_id": nid,
                    "title": title,
                    "cbf_score": float(item["score"]),
                    "ucb_score": 0.0,
                    "final_score": 0.3 * float(item["score"]),  
                    "mean_reward": 0.0,
                    "views": 0,
                    "clicks": 0,
                    "V_j": 0.0
                })
                continue

    
            mean = self._mean_reward(raw_rewards)
            vj = self._variance_vj(raw_rewards, t)
            ucb_score = self._ucb_tuned_score(raw_rewards, t)

            final_score = (0.7 * ucb_score) + (0.3 * float(item["score"]))

            ranked.append({
                "news_id": nid,
                "title": title,
                "cbf_score": float(item["score"]),
                "ucb_score": float(ucb_score),
                "final_score": float(final_score),
                "mean_reward": float(mean),
                "views": s,
                "clicks": sum(raw_rewards),
                "V_j": float(vj)
            })


        ranked.sort(key=lambda x: x["final_score"], reverse=True)

        return {
            "recommendations": ranked[:top_k],
            "all_ranked": ranked
        }


    def close(self):
        self.ucb_repo.close()