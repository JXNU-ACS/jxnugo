#-*- coding: UTF-8 -*-
from . import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager


class Role(db.Model):
    __tablename='roles'
    roleId=db.Column(db.Integer,primary_key=True)
    roleName=db.Column(db.String(20),unique=True)

    def __repr__(self):
        return '<Role %r>' % self.roleName

class User(UserMixin,db.Model):
    __tablename__='users'
    UserId=db.Column(db.Integer,primary_key=True,unique=True)
    userName=db.Column(db.String(20),index=True)
    userEmail=db.Column(db.String(20))
    userPasswordHash=db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.userName

    @property
    def password(self):
        raise AttributeError("password was not a  readable arrribute")

    @password.setter
    def password(self,password):
        self.userPasswordHash=generate_password_hash(password)

    def confim_password(self,password):
        return check_password_hash(self.userPasswordHash,password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
