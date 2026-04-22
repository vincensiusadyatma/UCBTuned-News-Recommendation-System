from src.repositories import RecommendationLogRepository


class RecommendationLogService:
    def __init__(self):
        self.repo = RecommendationLogRepository()

    def create_log(self, user_id: int, recommendations: list[int], relevants: list[int] = None):
        return self.repo.save(
            user_id=user_id,
            recommendations=recommendations,
            relevants=relevants or []
        )


    def get_logs_for_evaluation(self):
        logs = self.repo.get_all()

        return [
            {
                "user_id": log.user_id,
                "recommendations": log.recommendations,
                "relevants": log.relevants or []
            }
            for log in logs
        ]

    def get_user_logs(self, user_id: int):
        return self.repo.get_by_user(user_id)

    def get_latest_log(self, user_id: int):
        return self.repo.get_latest_by_user(user_id)

    def delete_log(self, log_id: int):
        return self.repo.delete(log_id)

    def clear_all(self):
        return self.repo.delete_all()

    def close(self):
        self.repo.close()