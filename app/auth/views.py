#-*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,flash,session,request
from . import auth
from ..models import User,Role,randomId
from .. import  db
from ..email import send_email
from .forms import loginForm,registerForm
from flask.ext.login import logout_user,login_required,login_user,current_user



@auth.route('/passport',methods=['POST','GET'])
def passport():
    loginform=loginForm()
    registerform=registerForm()
    return render_template('auth/passport.html',loginform=loginform,registerform=registerform)



@auth.route('/login',methods=['GET','POST'])
def login():
    loginform=loginForm()
    db.create_all()
    if loginform.validate_on_submit():
        user=User.query.filter_by(userName=loginform.userName.data).first()
        if user is not None and user.verify_passWord(loginform.passWord.data):
            login_user(user,loginform.rememberMe.data)
            session['name']=loginform.userName.data
            flash(u'login successful,regsussful','bg-success')
            return redirect(url_for('auth.passport'))
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
        regUser=User(id=userid,userName=registerform.userName.data,userEmail=registerform.email.data,passWord=registerform.passWord.data)
        db.session.add(regUser)
        db.session.commit()
        flash('register successful,Now you can check your email')
        token=regUser.generate_confirmation_token()
        send_email(regUser.userEmail,'激活你的账户',
                   'auth/email/confirm',User=regUser,token=token
                   )
        flash('confirm email has been sent to your mail server')
        return redirect(url_for('auth.passport'))
    else:
        flash('post info failed')
    return redirect(url_for('auth.passport'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('name',None)
    flash('flash message:logout successful')
    return redirect(url_for('auth.passport'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.trade_list'))
    if current_user.confirm(token):
        flash('successful confirm account')
    else:
        flash('confirm token invalid or has expired')
    return redirect('main.trade_list')


@auth.route('/confirm')
@login_required
def resend_email():
    token=current_user.generate_confirmation_token()
    send_email(current_user.userEmail,'激活你的账户','auth/email/confirm',User=current_user,token=token)
    flash('a new email has been sent to your email')
    return redirect(url_for('main.trade_list'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5]!='auth.' and request.endpoint !='static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.trade_list'))
    return render_template('auth/unconfirmed.html')




