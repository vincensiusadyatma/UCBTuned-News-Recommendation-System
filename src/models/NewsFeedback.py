from sqlalchemy import Column, Integer, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config import Base

class NewsFeedback(Base):
    __tablename__ = "news_feedbacks"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False)

    feedback = Column(SmallInteger, nullable=False)  

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="feedbacks")
    news = relationship("News", back_populates="feedbacks")

    def __repr__(self):
        return f"<NewsFeedback(user_id={self.user_id}, news_id={self.news_id}, feedback={self.feedback})>"