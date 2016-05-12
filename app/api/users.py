# -*- coding: UTF-8 -*-
from flask import jsonify,request
from authentication import auth
from ..models import User
from ..email import send_email
from . import api
from .. import db


@api. route('/api/user/<int:id>')
@auth.login_required
def get_user(id):
    user=User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/api/user_collectionpost/<int:id>')
@auth.login_required
def get_user_collectionpost(id):
    user=User.query.get_or_404(id)
    posts=user.collectionPost
    return jsonify({"collectionPost":[post.to_json() for post in posts]})


@api.route('/api/user_followers/<int:id>')
@auth.login_required
def user_followers(id):
    user=User.query.get_or_404(id)
    followers=user.followers.all()
    return jsonify({"followers":[follower.followers_to_json() for follower in followers]})


@api.route('/api/user_followed/<int:id>')
@auth.login_required
def user_followed(id):
    user=User.query.get_or_404(id)
    followeds=user.followed.all()
    return jsonify({"followed":[followed.followed_to_json() for followed in followeds]})


@api.route('/api/register/<int:id>')
def register():
    user=User.from_json(request.json)
    db.session.add(u)
    db.session.commit()
    token=user.generate_confirmation_token()
    send_email(regUser.userEmail,'激活你的账户',
                   'auth/email/confirm',User=user,token=token
                   )
    response=jsonify({"registerStatus":"successful"})
    response.status_code=200
    return response


@api.route('/api/user_posts/<int:id>')
def user_posts(id):
    user=User.query.get_or_404(id)
    posts=user.posts.all()
    return jsonify({"userPosts":[post.to_json() for post in posts]})


@api.route('/api/user_comments/<int:id>')
def user_comments(id):
    user=User.query.get_or_404(id)
    comments=user.comments.all()
    return jsonify({"userComments":[comment.userComment_to_json() for comment in comments]})