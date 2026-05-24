from src.config import Session
from src.models import News, NewsSimilarity


class CbfRepository:
    def __init__(self):
        self.session = Session()

    def get_all_news_ordered(self):
        return self.session.query(News).order_by(News.id.asc()).all()

    def get_news_by_id(self, news_id: int):
        return (
            self.session.query(News)
            .filter(News.id == news_id)
            .first()
        )

    def get_top_similar_news(self, news_id: int, top_k: int = 10):
        return (
            self.session.query(NewsSimilarity)
            .filter(NewsSimilarity.news_id == news_id)
            .order_by(NewsSimilarity.score.desc())
            .limit(top_k)
            .all()
        )

    def clear_similarity(self):
        self.session.query(NewsSimilarity).delete()
        self.session.commit()

    def insert_similarity(self, rows: list[dict]):
        objects = [
            NewsSimilarity(
                news_id=row["news_id"],
                similar_news_id=row["similar_news_id"],
                score=row["score"],
            )
            for row in rows
        ]
        self.session.bulk_save_objects(objects)
        self.session.commit()

    def close(self):
        self.session.close()