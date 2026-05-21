from src.config import Session
from src.models.News import News
from sqlalchemy import func

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
    
    def search_by_title(self, keyword: str, page: int = 1, per_page: int = 20):

        query = self.session.query(News).filter(
            func.lower(News.title).op("REGEXP")(f"\\b{keyword}\\b")
        ).order_by(News.time.desc())

        return query.offset((page - 1) * per_page).limit(per_page).all()

    def count_search(self, keyword: str):
        return self.session.query(News).filter(
            News.title.ilike(f"%{keyword}%")
        ).count()
    
    def create_news(self, title: str, content: str):
        new_news = News(
            title=title,
            content=content,
        )
        self.session.add(new_news)
        self.session.commit()
        return new_news
    

    def update_news(self, news_id: int, title: str = None, content: str = None):
        news = self.get_by_id(news_id)
        if not news:
            return None

        if title:
            news.title = title
        if content:
            news.content = content

        self.session.commit()
        return news