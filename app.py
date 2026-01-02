from flask import Flask
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)
