#-*- coding: UTF-8 -*-
from flask import render_template
from . import auth
from ..models import User,Role
from .. import  db
from .forms import loginForm

@auth.route('/login')
def login():
    loginform=loginForm()
    return render_template('auth/login.html',loginform=loginform)

@auth.route('/register')
def register():
    return render_template('auth/register.html')

@auth.route('/login_and_reg')
def login_and_reg():
    return render_template('auth/login_and_reg.html')

@auth.route('/passport')
def passport():
    return render_template('auth/passport.html')
