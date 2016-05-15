# -*- coding: UTF-8 -*-
from flask import jsonify,current_app,url_for,request,g
from .authentication import auth
from ..models import  Post,User,Comment
from . import api
from .. import db


@api.route('/api/posts')
def get_posts():
    page=request.args.get('page',1,type=int)
    pagination=Post.query.paginate(
        page,per_page=current_app.config["JXNUGO_POSTS_PER_PAGE"],
        error_out=False
    )
    posts=pagination.items
    prev=None
    if pagination.has_prev:
        prev=url_for('api.get_posts', page=page-1, _external=True)
    next=None
    if pagination.has_next:
        next=url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({'posts':[post.to_json() for post in posts],
                    'prev': prev,
                    'next': next,
                    'count': pagination.total
                    })


@api.route('/api/posts/<int:id>')
def get_post(id):
    post=Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/api/new_post',methods=['POST'])
def new_post():
    post=Post.from_json(request.json)
    post.author=g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@api.route('/api/comments/<int:id>')
def comments(id):
    post=Post.query.get_or_404(id)
    comments=post.comments.all()
    return jsonify({"comments":[comment.to_json() for comment in comments]})


@api.route('/api/collect',methods=['POST'])
def collect():
    collectInfo=request.json
    user=User.query.get_or_404(collectInfo['userId'])
    post=Post.query.get_or_404(collectInfo['postId'])
    user.collect(post)
    response=jsonify({"collectStatus":"successful"})
    response.status_code=200
    return response


@api.route('/api/uncollect',methods=['POST'])
def uncollect():
    collectInfo=request.json
    user=User.query.get_or_404(collectInfo['userId'])
    post=Post.query.get_or_404(collectInfo['postId'])
    user.uncollect(post)
    response=jsonify({"uncollectStatus":"successful"})
    response.status_code=200
    return response


@api.route('/api/new_comment',methods=['POST'])
@auth.login_required
def new_comment():
    commentInfo=request.json
    comment=Comment(body=commentInfo['body'],id=Post.query.count()+1,author_id=commentInfo['userId'],post_id=commentInfo['postId'])
    db.session.add(comment)
    db.session.commit()
    response=jsonify({"commentStatus":"successful"})
    response.status_code=200
    return response


@api.route('/api/judge_collect',methods=['POST'])
@auth.login_required
def judge_collect():
    judgeInfo=request.json
    user=User.query.get_or_404(judgeInfo['userId'])
    post=Post.query.get_or_404(judgeInfo['postId'])
    if user.is_collecting(post):
        message=1
    else:
        message=0
    response=jsonify({"collectInfo":message})
    response.status_code=200
    return response