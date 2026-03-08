from src.config import Session
from src.models.News import News

class NewsRepository:
    def __init__(self):
        self.session = Session()

    def get_all(self):
        return self.session.query(News).all()

    def get_all_by_page(self, page: int = 1, per_page: int = 20):
        query = self.session.query(News).order_by(News.time.desc())
        return query.offset((page - 1) * per_page).limit(per_page).all()

    def get_by_id(self, news_id: int):
        return self.session.query(News).filter(News.id == news_id).first()

    def get_by_link(self, link: str):
        return self.session.query(News).filter(News.link == link).first()

    def delete_news(self, news_id: int):
        news = self.get_by_id(news_id)
        if not news:
            return False
        self.session.delete(news)
        self.session.commit()
        return True
    
    def count_all(self):
        return self.session.query(News).count()