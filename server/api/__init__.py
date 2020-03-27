import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from api.config import app_config


db = SQLAlchemy()
cors = CORS()


def create_app(script_info=None):
    app = Flask(__name__)
    cors.init_app(app)
    config_name = os.environ.get('APP_SETTINGS', 'development')
    app.config.from_object(app_config.get(config_name))

    db.init_app(app)

    from api.blogs.blog import blog
    app.register_blueprint(blog)
    from api.blogs.auth import auth
    app.register_blueprint(auth)

    return app
