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
    db.create_all()
    if loginform.validate_on_submit():
        user=User.query.filter_by(userName=loginform.userName.data).first()
        if user is not None: #and user.verify_password(loginform.passWord.data):
            login_user(user,loginform.rememberMe.data)
            session['name']=loginform.userName.data
            flash(u'login successful,regsussful','bg-success')
            return redirect(url_for('main.trade_list'))
        else:
            flash(u'userName or userPassword uncorrect','bg-warning')
            return redirect(url_for('auth.passport'))
    return redirect(url_for('auth.passport'))


@auth.route('/register',methods=['GET','POST'])
def register():
    loginform=loginForm()
    registerform=registerForm()
    if registerform.validate_on_submit():
        userid=randomId()
        regUser=User(id=userid,userName=registerform.userName.data,userEmail=registerform.email.data,userPassword=registerform.passWord.data)
        db.session.add(regUser)
        db.session.commit()
        flash('register successful,Now you can login your account')
        return redirect(url_for('auth.passport'))
    else:
        flash('post info failed')
    return render_template("auth/passport.html",loginform=loginform,registerform=registerform)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('name',None)
    flash('flash message:logout successful')
    return redirect(url_for('auth.passport'))

@auth.route('/passport',methods=['POST','GET'])
def passport():
    loginform=loginForm()
    registerform=registerForm()
    return render_template('auth/passport.html',loginform=loginform,registerform=registerform)

