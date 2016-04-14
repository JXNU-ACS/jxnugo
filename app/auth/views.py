#-*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,flash,session,request
from . import auth
from ..models import User,Role,randomId
from .. import  db
from .forms import loginForm,registerForm
from flask.ext.login import logout_user,login_required,login_user

@auth.route('/login',methods=['GET','POST'])
def login():
    loginform=loginForm()
    registerform=registerForm()
    db.create_all()
    if loginform.validate_on_submit():
        user=User.query.filter_by(userName=loginform.userName.data).first()
        if user is not None: #and user.verify_password(loginform.passWord.data):
            login_user(user,loginform.rememberMe.data)
            session['name']=loginform.userName.data
            flash('flash message:login successful')
            return render_template('trade_list.html',name=session.get('name'))
        else:
            flash('userName or userPassword uncorrect')
    return render_template('auth/passport.html',loginform=loginform,registerform=registerform)

@auth.route('/register',methods=['GET','POST'])
def register():
    loginform=loginForm()
    registerform=registerForm()
    if registerform.validate_on_submit():
        flash('receive reg info successful')
        userid=111111111
        regUser=User(id=userid,userName=registerform.userName.data,userEmail=registerform.email.data,userPasswrod=registerform.confirm.data)
        db.session.add(regUser)
        db.session.commit()
        flash('register successful')
        return redirect(url_for('auth.passport'))
    else:
        flash('no register information post')
    return redirect(url_for('auth.passport'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('flash message:logout successful')
    return redirect(url_for('auth.passport'))

@auth.route('/passport',methods=['POST','GET'])
def passport():
    loginform=loginForm()
    registerform=registerForm()
    return render_template('auth/passport.html',loginform=loginform,registerform=registerform)

