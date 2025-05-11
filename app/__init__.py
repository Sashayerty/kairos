from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect

from app.ai_couch.routes import ai_couch
from app.api import ApiStatus, Check, GenerateCourse
from app.config import config
from app.models import UsersModel, create_session, global_init

login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    CSRFProtect(app=app)
    api = Api(app=app, prefix="/api")
    api.add_resource(GenerateCourse, "/gen")
    api.add_resource(Check, "/check")
    api.add_resource(ApiStatus, "/")
    app.config.from_object(config)
    login_manager.init_app(app)
    app.register_blueprint(ai_couch)
    global_init(db_file=app.config["DATABASE_PATH"])

    return app


@login_manager.user_loader
def load_user(user_id):
    db_ses = create_session()
    return db_ses.query(UsersModel).get(user_id)
