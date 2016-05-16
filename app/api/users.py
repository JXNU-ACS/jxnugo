# -*- coding: UTF-8 -*-
from flask import jsonify,request,g
from authentication import auth
from ..models import User
from ..email import send_email
from . import api
from .. import db


@api. route('/api/user/<int:id>')
def get_user(id):
    user=User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/api/user_collectionpost/<int:id>')
def get_user_collectionpost(id):
    user=User.query.get_or_404(id)
    posts=user.collectionPost
    return jsonify({"collectionPost":[post.to_json() for post in posts]})


@api.route('/api/user_followers/<int:id>')
def user_followers(id):
    user=User.query.get_or_404(id)
    followers=user.followers.all()
    return jsonify({"followers":[follower.followers_to_json() for follower in followers]})


@api.route('/api/user_followed/<int:id>')
def user_followed(id):
    user=User.query.get_or_404(id)
    followeds=user.followed.all()
    return jsonify({"followed":[followed.followed_to_json() for followed in followeds]})


@api.route('/api/register', methods=['POST'])
def register():
    userinfo=request.json
    print userinfo
    u=User(id=User.query.count()+1,userName=userinfo['userName'],userEmail=userinfo['userEmail'],passWord=userinfo['passWord'])
    db.session.add(u)
    db.session.commit()
    token=u.generate_confirmation_token()
    send_email(u.userEmail,'激活你的账户',
                   'auth/email/confirm',User=u,token=token
                   )
    response=jsonify({"registerStatus":"successful"})
    response.status_code=200
    return response


@api.route('/api/user_posts/<int:id>')
def user_posts(id):
    user=User.query.get_or_404(id)
    posts=user.posts.all()
    return jsonify({"userPosts":[post.to_json() for post in posts]})


@api.route('/api/test')
def test():
    return jsonify({"userName":"test","userEmail":"jxnuacs@qq.com","passWord":"123"})


@api.route('/api/user_comments/<int:id>')
def user_comments(id):
    user=User.query.get_or_404(id)
    comments=user.comments.all()
    return jsonify({"userComments":[comment.userComment_to_json() for comment in comments]})


@api.route('/api/follow', methods=['POST'])
@auth.login_required
def follow():
    followInfo=request.json
    self=User.query.get_or_404(followInfo['userId'])
    if g.current_user == self:
        followed=User.query.get_or_404(followInfo['followedId'])
        self.follow(followed)
        message="follow successful"
    else:
        message="you dont't hava right to do it"
    response=jsonify({"followStatus":message})
    response.status_code=200
    return response


@api.route('/api/unfollow', methods=['POST'])
@auth.login_required
def unfollow():
    followInfo=request.json
    self=User.query.get_or_404(followInfo['userId'])
    if g.current_user == self:
        unfollowUser=User.query.get_or_404(followInfo['unfollowedId'])
        self.unfollow(unfollowUser)
        message="unfollow successful"
    else:
        message="you don't hava right to do it"
    response=jsonify({"unfollowStatus":message})
    response.status_code=200
    return response


@api.route('/api/judge_follow',methods=['POST'])
@auth.login_required
def judge_follow():
    followInfo=request.json
    self=User.query.get_or_404(followInfo['userId'])
    follower=User.query.get_or_404(followInfo['followerId'])
    if self.is_following(follower):
        message=1
    else:
        message=0
    response=jsonify({"judgeInfo":message})
    response.status_code=200
    return response