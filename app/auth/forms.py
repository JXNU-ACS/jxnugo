#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Email,EqualTo,Length

class loginForm(Form):
    userName=StringField(validators=[Required()])
    passWord=PasswordField()
    rememberMe=BooleanField()
    submit=SubmitField(u'提交')


class registerForm(Form):
    userName=StringField(validators=[Required()])
    email=StringField(validators=[Email()])
    passWord=PasswordField(validators=[Required(),EqualTo('confirm')])
    confirm=PasswordField()
    submit=SubmitField('Submit')
