from flask import Flask
from src.config import Config

from src.routes import auth_bp, cbf_bp, ucb_tuned_bp,news_bp, recommendation_log_bp, evaluation_bp
from .cli import news_seeding, cbf_precompute, reset_database
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

def createApp():
    app = Flask(__name__)

    CORS(
        app,
        supports_credentials=True,
        origins=[os.getenv("FRONTEND_URL")]
    )
    
    app.config.from_object(Config)
    app.cli.add_command(news_seeding)
    app.cli.add_command(cbf_precompute)
    app.cli.add_command(reset_database)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cbf_bp)
    app.register_blueprint(ucb_tuned_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(recommendation_log_bp)
    app.register_blueprint(evaluation_bp)
 

    return app