#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from flask import flash
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Email,EqualTo,Length
from ..models import User
from wtforms import ValidationError

class loginForm(Form):
    userName=StringField(validators=[Required()])
    passWord=PasswordField(validators=[Required()])
    rememberMe=BooleanField(u'记住我')
    submit=SubmitField(u'登录')


class registerForm(Form):
    userName=StringField(validators=[Required()])
    email=StringField(validators=[Email(), Required()])
    passWord=PasswordField(validators=[Required(), EqualTo('confirm',message=u'两次密码必须一样')])
    confirm=PasswordField(validators=[Required()])
    submit=SubmitField(u'注册')

    def validate_email(self,field):
        if User.query.filter_by(userEmail=field.data).first():
            flash(u'该邮箱已经被使用,请更换后重新注册', 'bg-warning')
            raise ValidationError(u'该邮箱已经被注册')

    def validate_userName(self,field):
        if User.query.filter_by(userName=field.data).first():
            flash(u'该用户名已经被使用,请更换后重新注册', 'bg-warning')
            raise ValidationError(u'该用户名已经存在')