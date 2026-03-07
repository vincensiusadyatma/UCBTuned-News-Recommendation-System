from flask import Flask
from src.config import Config

from src.routes import auth_bp, cbf_bp, ucb_tuned_bp
from .cli import news_seeding, cbf_precompute
from flask_cors import CORS

def createApp():
    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    app.config.from_object(Config)
    app.cli.add_command(news_seeding)
    app.cli.add_command(cbf_precompute)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cbf_bp)
    app.register_blueprint(ucb_tuned_bp)
 

    return app