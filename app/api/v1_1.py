# -*- coding: UTF-8 -*-
from flask import jsonify, request, abort, current_app
from authentication import auth
from ..models import User, getPrimaryKeyId, Comment, Post
from ..email import send_email
from . import api
from .. import db
from errors import bad_request, NotAccept, ResourceConflict


@api.route('/apiv1.1/register', methods=['POST'])
def register_v11():
    userinfo = request.json
    if userinfo['auth_token'] != current_app.config['AUTH_TOKEN']:
        return bad_request('auth_token not correct')
    if userinfo['userName'] == '' or userinfo['userEmail'] == '' or userinfo['passWord'] == '':
        return bad_request('userInfo was empty')
    user_by_email = User.query.filter_by(userEmail=userinfo['userEmail']).first()
    user_by_name = User.query.filter_by(userName=userinfo['userName']).first()
    if user_by_name is not None:
        return NotAccept('userName was aleady exist')
    if user_by_email is not None:
        return ResourceConflict('email was aleady exist')
    u = User(id=getPrimaryKeyId('isUser'), name='jxnugo_'+str(getPrimaryKeyId('isUser')), userName=userinfo['userName'], userEmail=userinfo['userEmail'],passWord=userinfo['passWord'])
    db.session.add(u)
    db.session.commit()
    token = u.generate_confirmation_token()
    send_email(u.userEmail, '激活你的账户',
                   'auth/email/confirm', User=u, token=token
                   )
    response = jsonify({"registerStatus":"successful"})
    response.status_code = 200
    return response


@api.route('/apiv1.1/new_post', methods=['POST'])
@auth.login_required
def new_post_v11():
    postInfo = request.json
    if postInfo['auth_token'] != current_app.config['AUTH_TOKEN']:
        return bad_request('auth_token not correct')
    user = User.query.get_or_404(postInfo['userId'])
    photo = postInfo['photos']
    l = []
    for x in range(0, len(photo)):
        temp = photo[x]['key']
        l.append(temp)
    photos = ":".join(l)
    post = Post(id=getPrimaryKeyId('isPost'), body=postInfo['body'], goodName=postInfo['goodsName'],
                goodPrice=postInfo['goodsPrice'], goodLocation=postInfo['goodsLocation'],
                goodQuality=postInfo['goodsQuality'], goodBuyTime=postInfo['goodsBuyTime'], goodTag=postInfo['goodsTag'],
                contact=postInfo['contact'],
                author_id=user.id, photos=photos, goodNum=postInfo['goodsNum'])
    db.session.add(post)
    db.session.commit()
    response = jsonify({"postStatus": "successful"})
    response.status_code = 200
    return response


@api.route('/apiv1.1/new_comment', methods=['POST'])
@auth.login_required
def new_comment_v11():
    commentInfo = request.json
    if commentInfo['auth_token'] != current_app.config['AUTH_TOKEN']:
        return bad_request('auth_token not correct')
    if commentInfo['body'] == '':
        return bad_request('body was empty')
    comment = Comment(body=commentInfo['body'], author_id=commentInfo['userId'],
                      post_id=commentInfo['postId'])
    db.session.add(comment)
    db.session.commit()
    message = "successful"
    response = jsonify({"commentStatus": message})
    response.status_code = 200
    return response


@api.route('/apiv1.1/update_userInfo', methods=['POST'])
@auth.login_required
def update_userInfo_v11():
    userInfo = request.json
    if userInfo['auth_token'] != current_app.config['AUTH_TOKEN']:
        return bad_request('auth_token not correct')
    user = User.query.get_or_404(userInfo['userId'])
    user.name = userInfo['name']
    user.location = userInfo['location']
    user.sex = userInfo['sex']
    user.about_me = userInfo['about_me']
    user.contactMe = userInfo['contact']
    user.avatar = userInfo['avatar']
    db.session.add(user)
    db.session.commit()
    response = jsonify({"updateStatus":"successful"})
    response.status_code = 200
    return response


@api.route('/apiv1.1/post_delete', methods=['POST'])
@auth.login_required
def post_delete_v11():
    postInfo = request.json
    if postInfo['auth_token'] != current_app.config['AUTH_TOKEN']:
        return bad_request('auth_token not correct')
    p = Post.query.get_or_404(postInfo['postId'])
    if p is None:
        message = "the post dosen't exist"
    else:
        comments = Comment.query.filter_by(post_id=p.id).all()  # 删除评论
        for comment in comments:
            db.session.delete(comment)
        all_user = User.query.all()     # 删除收藏的关系
        for user in all_user:
            if p in user.collectionPost.all():
                user.collectionPost.remove(p)
            else:
                pass
        db.session.delete(p)
        db.session.commit()
        message = "successful delete post"
    response = jsonify({"deleteStatus": message})
    response.status_code = 200
    return response
