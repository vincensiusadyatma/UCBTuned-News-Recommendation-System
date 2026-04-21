from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.config import Base

class NewsSimilarity(Base):
    __tablename__ = "news_similarity"

    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    similar_news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)

    news = relationship("News", foreign_keys=[news_id], back_populates="similarities")
    similar_news = relationship("News", foreign_keys=[similar_news_id])