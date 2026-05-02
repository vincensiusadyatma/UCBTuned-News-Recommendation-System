from src.repositories import NewsRepository

class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()

    def get_all_news(self):
        return self.news_repo.get_all()
    

    def get_all_news_by_page(self, page: int = 1, per_page: int = 20):
        return self.news_repo.get_all_by_page(page, per_page)

   
    def get_news_by_id(self, news_id: int):
        news = self.news_repo.get_by_id(news_id)
        if not news:
            raise ValueError(f"News with ID {news_id} not found")
        return news
    

    def delete_news(self, news_id: int):
        success = self.news_repo.delete_news(news_id)
        if not success:
            raise ValueError(f"News with ID {news_id} not found")
        return success
    
    def get_total_pages(self, per_page: int = 20):
        total_items = self.news_repo.count_all()
        total_pages = (total_items + per_page - 1) // per_page  
        return total_pages
    

    def search_news(self, keyword: str, page: int = 1, per_page: int = 20):
        return self.news_repo.search_by_title(keyword, page, per_page)


    def get_search_total_pages(self, keyword: str, per_page: int = 20):
        total_items = self.news_repo.count_search(keyword)
        total_pages = (total_items + per_page - 1) // per_page
        return total_pages
    

    def create_news(self, title: str, content: str):
        if not title or not content:
            raise ValueError("Title dan content tidak boleh kosong")

        return self.news_repo.create_news(title, content)
    

    def update_news(self, news_id: int, title: str = None, content: str = None):
        if not title and not content:
            raise ValueError("Minimal salah satu field harus diisi (title/content)")

        updated_news = self.news_repo.update_news(news_id, title, content)
        if not updated_news:
            raise ValueError(f"News with ID {news_id} not found")

        return updated_news
    

    def delete_news(self, news_id: int):
        success = self.news_repo.delete_news(news_id)
        if not success:
            raise ValueError(f"News with ID {news_id} not found")
        return success