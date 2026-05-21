from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship(
        "User",
        back_populates="role"
    )

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"