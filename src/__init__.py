from flask import Flask
from src.config import Config

from src.routes import auth_bp

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
 

    return app