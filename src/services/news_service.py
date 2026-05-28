from src.repositories import NewsRepository
from src.repositories import NewsRepository
from src.services.preprocessing_service import PreprocessingService
from src.services.cbf_service import CbfService

import pandas as pd
import os

class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()

        self.preprocessor = PreprocessingService()

        self.cbf_service = CbfService()

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

        news = self.news_repo.create_news(
            title,
            content
        )

        preprocess_title = self.preprocessor.preprocess(title)
        preprocess_content = self.preprocessor.preprocess(content)

   
        self.append_preprocessed_csv(
            news.id,
            preprocess_title,
            preprocess_content
        )

        self.cbf_service.compute_similarity()
        return news
    
    def append_preprocessed_csv(self,news_id,title,content):
        path = "dataset/news_preprocess.csv"

        new_row = {
            "news_id": news_id,
            "Judul": title,
            "Content": content
        }

     
        if os.path.exists(path):
            df = pd.read_csv(path)
            df_new = pd.DataFrame([new_row])
            df = pd.concat(
                [df, df_new],
                ignore_index=True
            )
        else:
            df = pd.DataFrame([new_row])

        df.to_csv(path, index=False)
    

    def update_news(self,news_id: int,title: str = None,content: str = None):
        if not title and not content:
            raise ValueError(
                "Minimal salah satu field harus diisi"
            )

        updated_news = self.news_repo.update_news(news_id,title,content)

        if not updated_news:
            raise ValueError(
                f"News with ID {news_id} not found"
            )

        preprocess_title = self.preprocessor.preprocess(updated_news.title)

        preprocess_content = self.preprocessor.preprocess(updated_news.content)

        self.update_preprocessed_csv(news_id,preprocess_title,preprocess_content)

        self.cbf_service.compute_similarity()

        return updated_news
    
    def delete_preprocessed_csv(self, news_id):
        path = "dataset/news_preprocess.csv"

        if not os.path.exists(path):
            raise ValueError(
                "CSV preprocess tidak ditemukan"
            )

        df = pd.read_csv(path)
        df = df[df["news_id"] != news_id]
        df.to_csv(path, index=False)
    

    def delete_news(self, news_id: int):
        success = self.news_repo.delete_news(news_id)

        if not success:
            raise ValueError(
                f"News with ID {news_id} not found"
            )
        self.delete_preprocessed_csv(news_id)
        self.cbf_service.compute_similarity()

        return success
    
    def update_preprocessed_csv(self,news_id,title,content):
        path = "dataset/news_preprocess.csv"

        if not os.path.exists(path):
            raise ValueError("CSV preprocess tidak ditemukan")

        df = pd.read_csv(path)
        index = df[df["news_id"] == news_id].index

        if len(index) == 0:
            raise ValueError(
                f"news_id {news_id} tidak ditemukan di CSV"
            )

        df.loc[index, "Judul"] = title
        df.loc[index, "Content"] = content
        df.to_csv(path, index=False)