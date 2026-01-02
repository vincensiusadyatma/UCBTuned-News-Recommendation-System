import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

class Config():
    DEBUG = os.getenv("APP_DEBUG", "False") == "True"
    ENV = os.getenv("APP_ENV", "production")
    DB =  os.getenv("DATABASE_URL")
    PORT = int(os.getenv("PORT", 5000))
    DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    Testing = False
    






