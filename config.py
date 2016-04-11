#-*- coding: UTF-8 -*-
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'the string was hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    FLASKY_MAIL_SUBJECT_PREFIX='[JxnuGo]'
    FLASK_MAIL_SENDER='jxnugo@163.com'
    FLASK_ADMIN=os.environ.get('FLASK_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.163.com'
    MAIL_PORT=25
    MAIL_USER_TLS=True
    MAIL_USERNAME=os.environ.get('jxnugo@163.com')
    MAIL_PASSWORD=os.environ.get('')
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
    #SQLALCHEMY_DATABASE_URL=mysql://root:ldl8571001@139.129.52.83:3306/testmysql #os.environ.get('DEVELOPMENT_DATABASE_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URL=os.environ.get('TESTING_DATABASE_URL')



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URL=os.environ.get('PRODUCTION_DATABASE_URL')


config={
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default':DevelopmentConfig

}