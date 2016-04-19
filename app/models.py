#-*- coding: UTF-8 -*-
from . import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
import random
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Role(db.Model):
    __tablename__='Role'
    roleId=db.Column(db.Integer,primary_key=True)
    roleName=db.Column(db.String(20),unique=True)

    def __repr__(self):
        return '<Role %r>' % self.roleName

class User(UserMixin,db.Model):
    __tablename__='User'
    id=db.Column(db.Integer,primary_key=True,unique=True)
    userName=db.Column(db.String(20),index=True)
    userEmail=db.Column(db.String(30))
    userPasswordHash=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)

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




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def randomId():
    l='1'
    for x in range(0,9):
	        a=int(random.uniform(0,9))
	        z=str(a)
	        l=l+z
    return l