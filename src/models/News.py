from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.config import Base
from sqlalchemy.orm import relationship

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    time = Column(DateTime, default=datetime.utcnow, nullable=False)
    content = Column(Text, nullable=False)
    similarities = relationship(
        "NewsSimilarity",
        foreign_keys="NewsSimilarity.news_id",
        back_populates="news",
        cascade="all, delete-orphan"
    )

    feedbacks = relationship(
        "NewsFeedback",
        back_populates="news",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<News(title='{self.title}', source='{self.source}')>"
