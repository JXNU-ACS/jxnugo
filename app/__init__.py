#-*- coding: UTF-8 -*-
from flask import Flask
from flask.ext.moment import Moment
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import configs, ENV

mail=Mail()
moment=Moment()
db=SQLAlchemy()
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'


def create_app():
    app=Flask(__name__)
    app.config.from_object(configs[ENV])
    configs[ENV].init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,urlfix='/auth')
    from .trade import trade as trade_blueprint
    app.register_blueprint(trade_blueprint,urlfix='/trade')
    from .bbs import bbs as bbs_blueprint
    app.register_blueprint(bbs_blueprint,urlfix='/bbs')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint,urlfix='/api')
    login_manager.init_app(app)
    return app

