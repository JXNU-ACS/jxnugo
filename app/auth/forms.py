#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Email,EqualTo,Length

class loginForm(Form):
    userName=StringField(validators=[Required()])
    passWord=PasswordField(validators=[Required()])
    rememberMe=BooleanField(u'记住我')
    submit=SubmitField(u'登录')


class registerForm(Form):
    userName=StringField(validators=[Required()])
    email=StringField(validators=[Email(),Required()])
    passWord=PasswordField(validators=[Required(),EqualTo('confirm',message=u'两次密码必须一样')])
    confirm=PasswordField(validators=[Required()])
    submit=SubmitField(u'注册')
