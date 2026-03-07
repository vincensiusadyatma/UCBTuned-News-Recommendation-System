from src.config import Session
from src.models import NewsFeedback


class UcbTunedRepository:
    def __init__(self):
        self.session = Session()

    def get_feedback_by_news_ids(self, news_ids: list[int]):
        if not news_ids:
            return {}

        rows = (
            self.session.query(
                NewsFeedback.news_id,
                NewsFeedback.feedback
            )
            .filter(NewsFeedback.news_id.in_(news_ids))
            .all()
        )

        stats = {}
        for news_id, feedback in rows:
            if news_id not in stats:
                stats[news_id] = {"rewards": []}

            stats[news_id]["rewards"].append(1 if feedback > 0 else 0)

        return stats

    def close(self):
        self.session.close()