from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.dialects.mysql import JSON
from datetime import datetime
from src.config import Base


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recommendations = Column(JSON, nullable=False)

    relevants = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)