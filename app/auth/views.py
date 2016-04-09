#-*- coding: UTF-8 -*-
from flask import render_template
from . import auth
from ..models import User,Role
from .. import  db
from .forms import loginForm

@auth.route('/login')
def login():
    loginform=loginForm()
    return render_template('login.html',loginform=loginform)

@auth.route('/register')
def register():
    return render_template('register.html')
