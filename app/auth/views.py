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
            return redirect(url_for('main.trade_list'))
        else:
            flash(u'用户名或密码错误','bg-warning')
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
        token=regUser.generate_confirmation_token()
        send_email(regUser.userEmail,'激活你的账户',
                   'auth/email/confirm',User=regUser,token=token
                   )
        flash(u'注册成功,账户激活信息已经发送到您的邮件!')
        return redirect(url_for('auth.passport'))
    return redirect(url_for('auth.passport'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('name',None)
    flash(u'成功推出账户')
    return redirect(url_for('auth.passport'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.trade_list'))
    if current_user.confirm(token):
        flash(u'恭喜您完成账户验证')
    else:
        flash(u'验证信息已过期,请申请系统重新发送邮件')
    return redirect('trade_list')


@auth.route('/confirm')
@login_required
def resend_email():
    token=current_user.generate_confirmation_token()
    send_email(current_user.userEmail,'激活你的账户','auth/email/confirm',User=current_user,token=token)
    flash(u'激活邮件已经发送到您的账户')
    return redirect(url_for('main.trade_list'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5]!='auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.trade_list'))
    return render_template('auth/unconfirmed.html')



