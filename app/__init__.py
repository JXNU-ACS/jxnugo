#-*- coding: UTF-8 -*-
from flask import Flask
from flask.ext.moment import Moment
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

mail=Mail()
moment=Moment()
db=SQLAlchemy()
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'

def create_app():
    app=Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)

    moment.init_app(app)
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()

    return app