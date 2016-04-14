#-*- coding: UTF-8 -*-
from . import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from random import uniform


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
    userPassword=db.Column(db.String(30))

    def __repr__(self):
        return '<User %r>' % self.userName

    @property
    def password(self):
        raise AttributeError("password was not a  readable arrribute")

    @password.setter
    def password(self,password):
        self.userPasswordHash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.userPasswordHash,password)

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