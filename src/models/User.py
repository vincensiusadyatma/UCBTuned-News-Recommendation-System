from sqlalchemy import Column, Integer, String
from config import Base

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self) -> str:
            return f"User(id={self.id!r}, username={self.username!r})"

