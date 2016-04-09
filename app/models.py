#-*- coding: UTF-8 -*-
from . import db
from . import login_manager

class Role(db.Model):
    __tablename='roles'
    roleId=db.Column(db.Integer,primary_key=True)
    roleName=db.Column(db.String(20),unique=True)

    def __repr__(self):
        return '<Role %r>' % self.roleName

class User(db.Model):
    __tablename__='users'
    UserId=db.Column(db.Integer,primary_key=True,unique=True)
    userName=db.Column(db.String(20),index=True)
    userEmail=db.Column(db.String(20))
    userPasswordHash=db.Column(db.String(128))


    def __repr__(self):
        return '<User %r>' % self.userName


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
