# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:29
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from config import config


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
db = SQLAlchemy()
bootstrap = Bootstrap()
socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    socketio.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

