# -*- coding: UTF-8 -*-
from flask import jsonify,request,current_app,url_for
from .authentication import auth
from ..models import  Post
from . import api


@api.route('/api/posts')
@auth.login_required
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
@auth.login_required
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
