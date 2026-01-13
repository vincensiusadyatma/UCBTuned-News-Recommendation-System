from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import Config


engine = create_engine(Config.DB_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
