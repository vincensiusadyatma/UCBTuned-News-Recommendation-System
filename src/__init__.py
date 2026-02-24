from flask import Flask
from src.config import Config

from src.routes import auth_bp
from .cli import news_seeding, cbf_precompute
def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.cli.add_command(news_seeding)
    app.cli.add_command(cbf_precompute)
    app.register_blueprint(auth_bp)
 

    return app