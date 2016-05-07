# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, session, flash, views,current_app,jsonify
from ..decorators import admin_required, permission_required
from . import main
from .. import db
from forms import EditProfileForm, EditProfileAdminForm
from flask.ext.login import login_required, current_user
from ..models import Permission, User, Role, Post
from qiniu import Auth,put_file,etag,urlsafe_base64_encode
import qiniu.config
from uuid import uuid4

@main.route('/')
def indexof():
    return render_template('index.html')


@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/test')
@login_required
@admin_required
@permission_required(Permission.MODERATE_COMMENTS)
def test():
    return "for comment permission"


@main.route('/static/<filename>', methods=['GET'])
def staticfile(filename):
    url_for("static", filename)
    return redirect("base.html")


@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(userName=username).first()
    if user is None:
        abort(404)
    return render_template('info/user.html', user=user)


@main.route('/user_zone/<username>')
def user_zone(username):
    user = User.query.filter_by(userName=username).first()
    posts = Post.query.filter_by(author_id=user.id).all()
    if user is None:
        abort(404)
    return render_template('info/user_zone.html', user=user, posts=posts)


@main.route('/editUserInfo', methods=['GET', 'POST'])
@login_required
def editUserInfo():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.userName = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'修改个人信息成功')
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('info/editUserInfo.html', form=form)


@main.route('/show_user',methods=['GET','POST'])
@login_required
@admin_required
def show_user():
    users=User.query.all()
    return render_template('info/show_user.html', users=users)



@main.route('/editUserInfoAdmin/<pid>', methods=['GET', 'POST'])
@login_required
@admin_required
def editUserInfoAdmin(pid):
    user = User.query.get_or_404(pid)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.userEmail = form.email.data
        user.userName = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.locati = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash(u'已将个人信息更新')
        return render_template('info/editUserInfoAdmin.html',form=form,pid=user.id)
    form.email.data = user.userEmail
    form.username.data = user.userName
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('info/editUserInfoAdmin.html',form=form,pid=user.id)


@main.route('/get_upload_token')
def get_upload_token():
    q=Auth(current_app.config['QINIU_ACCESS_KEY'],current_app.config['QINIU_SECRET_KEY'])
    bucket_name='trade'
    key=uuid4()
    upload_token=q.upload_token(bucket_name,key,3600)
    return jsonify({'upload_token':upload_token,'key':key})

