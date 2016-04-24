#-*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,session,flash
from ..decorators import admin_required,permission_required
from . import main
from .. import db
from forms import EditProfileForm,EditProfileAdminForm
from flask.ext.login import login_required,current_user
from ..models import Permission,User,Role

@main.route('/trade_list')
def trade_list():
    return render_template('trade_list.html')

@main.route('/trade_detail')
def trade_detail():
    return render_template("trade_detail.html")

@main.route('/trade_post')
def trade_post():
    return render_template("trade_post.html")

<<<<<<< HEAD
@main.route('/test')
@login_required
@admin_required
@permission_required(Permission.MODERATE_COMMENTS)
def test():
    return "for comment permission"


@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(userName=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

@main.route('/editUserInfo',methods=['GET','POST'])
@login_required
def editUserInfo():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        flash(u'修改个人信息成功')
    form.name.data=current_user.name
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template('editUserInfo.html',form=form)

@main.route('/editUserInfo/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def editUserInfoAdmin(id):
    user=User.query.get_or_404(id)
    form=EditProfileAdminForm(user=user)
    if form .validate_on_submit():
        user.userEmail=form.email.data
        user.userName=form.username.data
        user.confirmed=form.confirmed.data
        user.role=Role.query.get(form.role.data)
        user.name=form.name.data
        user.locati=form.location.data
        user.about_me=form.about_me.data
        db.session.add(user)
        flash(u'已将个人信息更新')
        return redirect(url_for('.user',username=user.userName))
    form.email.data=user.userEmail
    form.username.data=user.userName
    form.confirmed.data=user.confirmed
    form.role.data=user.role_id
    form.name.data=user.name
    form.location.data=user.location
    form.about_me.data=user.about_me
    return render_template('editUserInfo.html',form=form,user=user)
=======
@main.route('/user_zone')
def user_zone():
    return render_template("user_zone.html")
>>>>>>> origin/master
