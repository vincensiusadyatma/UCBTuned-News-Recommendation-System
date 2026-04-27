from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)

   
    feedbacks = relationship(
        "NewsFeedback",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    evaluations = relationship(
        "EvaluationResult",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    recommendation_logs = relationship(
        "RecommendationLog",
        backref="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"