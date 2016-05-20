#-*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,flash,session,request,abort
from . import auth
from ..models import User,getPrimaryKeyId
from .. import db
from ..email import send_email
from .forms import loginForm,registerForm
from flask.ext.login import logout_user,login_required,login_user,current_user
from itsdangerous import JSONWebSignatureSerializer as Serializer
from config import configs,ENV


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
            return redirect(url_for('main.index'))
        else:
            flash(u'用户名或密码错误','bg-warning')
            return redirect(url_for('auth.passport',_external=True))
    return redirect(url_for('auth.passport',_external=True))


@auth.route('/register',methods=['GET','POST'])
def register():
    registerform=registerForm()
    if registerform.validate_on_submit():
        regUser=User(id=getPrimaryKeyId('isUser'), userName=registerform.userName.data,userEmail=registerform.email.data,passWord=registerform.passWord.data)
        db.session.add(regUser)
        db.session.commit()
        token=regUser.generate_confirmation_token()
        send_email(regUser.userEmail,'激活你的账户',
                   'auth/email/confirm',User=regUser,token=token
                   )
        flash(u'注册成功,账户激活信息已经发送到您的邮件!')
        return redirect(url_for('auth.passport', _external=True))
    return redirect(url_for('auth.passport', _external=True))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('name',None)
    flash(u'成功推出账户')
    return redirect(url_for('auth.passport'))


@auth.route('/confirm/<token>')
def confirm(token):
    s=Serializer(configs[ENV].SECRET_KEY)
    try:
        recvData=s.loads(token)
    except:
        abort(404)
    RecvId=recvData.get('confirm')
    u = User.query.filter_by(id=RecvId).first_or_404()
    u.confirmed=True
    db.session.add(u)
    db.session.commit()
    flash(u'恭喜您完成账号激活')
    return redirect(url_for('auth.passport'))


@auth.route('/confirm')
@login_required
def resend_email():
    token=current_user.generate_confirmation_token()
    send_email(current_user.userEmail,'激活你的账户','auth/email/confirm',User=current_user,token=token)
    flash(u'激活邮件已经发送到您的账户')
    return redirect(url_for('trade.trade_list'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5]!='auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('trade.trade_list'))
    return render_template('auth/unconfirmed.html')



