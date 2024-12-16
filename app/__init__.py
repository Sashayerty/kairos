from flask import Flask
from .config import config
from app.ai_couch.routes import ai_couch


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(ai_couch)
    return app
