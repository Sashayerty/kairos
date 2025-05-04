from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from app.ai_couch.routes import ai_couch
from app.api import Check, GenerateCourse
from app.config import config
from app.models import UsersModel, create_session, global_init

login_manager = LoginManager()

db_ses = create_session()


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app=app, prefix="/api")
    api.add_resource(GenerateCourse, "/gen")
    api.add_resource(Check, "/check")
    global_init("./app/kairos.db")
    app.config.from_object(config)
    login_manager.init_app(app)
    app.register_blueprint(ai_couch)
    return app


@login_manager.user_loader
def load_user(user_id):
    return db_ses.query(UsersModel).get(user_id)
