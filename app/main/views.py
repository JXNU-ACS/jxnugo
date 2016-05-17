# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, session, flash, views,current_app,jsonify,request
from ..decorators import admin_required, permission_required
from . import main
from .. import db
from forms import EditProfileForm, EditProfileAdminForm
from flask.ext.login import login_required, current_user
from ..models import Permission, User, Role, Post,Follow,collectionPosts
from qiniu import Auth,put_file,etag,urlsafe_base64_encode
import qiniu.config
from uuid import uuid4


@main.context_processor
def user_processor():
    def username(pid):
        return User.query.filter_by(id=pid).first().userName
    return dict(username=username)

@main.route('/')
def indexof():
    return render_template('index.html')


@main.route('/index')
def index():
    real_ip = request.headers.get('X-Real-Ip', request.remote_addr)
    print real_ip
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
    user = User.query.filter_by(userName=username).first()
    if user is None:
        abort(404)
    return render_template('info/user.html', user=user)


@main.route('/user_zone/<username>')
def user_zone(username):
    user = User.query.filter_by(userName=username).first()
    followersTen=user.followers.limit(10)
    followingTen=user.followed.limit(10)
    followersAll=user.followers.all()
    followingAll=user.followed.all()
    postFive=Post.query.filter_by(author_id=user.id).limit(5)
    collectionFive=user.collectionPost.limit(5)
    collectionAll=user.collectionPost.all()
    posts = Post.query.filter_by(author_id=user.id).all()
    if user is None:
        abort(404)

    return render_template('info/user_zone.html',user=user, posts=posts,postFive=postFive,collectionAll=collectionAll,collectionFive=collectionFive, followersTen=followersTen, followersAll=followersAll, followingTen=followingTen,followingAll=followingAll)


@main.route('/editUserInfo', methods=['GET', 'POST'])
@login_required
def editUserInfo():
    form = EditProfileForm()
    user=current_user
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
    return render_template('info/editUserInfo.html', form=form,user=user)


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


@main.route('/get_upload_token',methods=['GET'])
def get_upload_token():
    q=Auth(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_SECRET_KEY'])
    bucket_name='trade'
    key=None
    policy={
         "scope": "trade"
    }

    upload_token=q.upload_token(bucket_name,key,3600,policy)
    return jsonify({'uptoken': upload_token})


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user=User.query.filter_by(userName=username).first()
    if user is None:
        flash(u'没有该用户,关注失败')
    if current_user.is_following(user):
        flash(u'你已经关注过该用户,无需再次关注')
        return redirect(url_for('trade.trade_list'))
    current_user.follow(user)
    flash(u'成功关注%s' % username)
    return redirect(url_for('main.user_zone',username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user=User.query.filter_by(userName=username).first()
    if user is None:
        flash(u'没有该用户')
    current_user.unfollow(user)
    flash(u'成功取消对%s的关注' % username)
    return redirect(url_for('main.user_zone',username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(userName=username).first()
    if user is None:
        flash(u'该用户不存在')
        return redirect(url_for('trade.trade_list'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['JXNUGO_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('info/followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows,)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(userName=username).first()
    if user is None:
        flash(u'该用户不存在')
        return redirect(url_for('trade.trade_list'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['JXNUGO_FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user':item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('info/followed.html', user=user, title=u'关注他的',
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows,)
