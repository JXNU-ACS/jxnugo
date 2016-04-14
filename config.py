#-*- coding: UTF-8 -*-
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'the string was hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    FLASKY_MAIL_SUBJECT_PREFIX='[JxnuGo]'
    FLASK_MAIL_SENDER='jxnugo@163.com'
    FLASK_ADMIN=os.environ.get('FLASK_ADMIN')
    SQLALCHEMY_DATABASE_URI= 'mysql://root:laidaolong@localhost:3306/jxnugo'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.163.com'
    MAIL_PORT=25
    MAIL_USER_TLS=True
    MAIL_USERNAME=os.environ.get('jxnugo@163.com')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URL='mysql://root:laidaolong@localhost:3306/jxnugo'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URL='mysql://root:laidaolong@localhost:3306/jxnugo'



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URL='mysql://root:laidaolong@localhost:3306/jxnugo'


config={
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default':DevelopmentConfig

}