#-*- coding: UTF-8 -*-
from . import db
from flask.ext.login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
import random
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    home = db.Column(db.String(64), unique=True)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True,unique=True)
    userName=db.Column(db.String(20),index=True)
    userEmail=db.Column(db.String(30))
    userPasswordHash=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    name=db.Column(db.String(64))
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    menber_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)


    def __repr__(self):
        return '<User %r>' % self.userName

    #check password by passWordHash
    @property
    def passWord(self):
        raise AttributeError("passWord was not a  readable arrribute")

    @passWord.setter
    def passWord(self,passWord):
        self.userPasswordHash=generate_password_hash(passWord)

    def verify_passWord(self,passWord):
        return check_password_hash(self.userPasswordHash,passWord)

    #confirm account when user register
    def generate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm') !=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True

    #role and permissions
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.userEmail==current_app.config['JXNUGO_ADMIN']:
                self.role=Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()

    def can(self,permissions):
        return self.role is not None and (self.role.permissions & permissions)==permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    #user information
    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)

class AnonymousUser(AnonymousUserMixin):
    def can(self,perimissions):
        return False
    def is_administrator(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.anonymous_user=AnonymousUser
def randomId():
    l='1'
    for x in range(0,9):
	        a=int(random.uniform(0,9))
	        z=str(a)
	        l=l+z
    return l