# -*- coding: UTF-8 -*-
from flask import jsonify, current_app, url_for, request, g
from .authentication import auth
from ..models import Post, User, Comment, getPrimaryKeyId
from . import api
from .. import db
from .errors import bad_request


@api.route('/api/posts')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["JXNUGO_POSTS_PER_PAGE"],
        error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page - 1, _external=True)
        # prev="http://www.jxnugo.com/api/posts?page=%d" % (page-1)
    next = None
    if pagination.has_next:
        # next="http://www.jxnugo.com/api/posts?page=%d" % (page+1)
        next = url_for('api.get_posts', page=page + 1, _external=True)
    return jsonify({'posts': [post.to_json() for post in posts],
                    'prev': prev,
                    'next': next,
                    'count': pagination.total
                    })


@api.route('/api/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/api/comments/<int:id>')
def comments(id):
    post = Post.query.get_or_404(id)
    comments = post.comments.order_by(Comment.timestamp)
    return jsonify({"comments": [comment.to_json() for comment in comments]})


@api.route('/api/collect', methods=['POST'])
def collect():
    collectInfo = request.json
    user = User.query.get_or_404(collectInfo['userId'])
    post = Post.query.get_or_404(collectInfo['postId'])
    user.collect(post)
    message = "collect successful"
    response = jsonify({"collectStatus": message})
    response.status_code = 200
    return response


@api.route('/api/uncollect', methods=['POST'])
def uncollect():
    collectInfo = request.json
    user = User.query.get_or_404(collectInfo['userId'])
    post = Post.query.get_or_404(collectInfo['postId'])
    user.uncollect(post)
    message = "uncollect successful"
    response = jsonify({"uncollectStatus": message})
    response.status_code = 200
    return response


@api.route('/api/new_comment', methods=['POST'])
@auth.login_required
def new_comment():
    commentInfo = request.json
    if commentInfo['body'] == '':
        return  bad_request('body was empty')
    comment = Comment(id=Comment.query.count() + 1, body=commentInfo['body'], author_id=commentInfo['userId'],
                          post_id=commentInfo['postId'])
    db.session.add(comment)
    db.session.commit()
    message = "successful"
    response = jsonify({"commentStatus": message})
    response.status_code = 200
    return response


@api.route('/api/judge_collect', methods=['POST'])
@auth.login_required
def judge_collect():
    judgeInfo = request.json
    user = User.query.get_or_404(judgeInfo['userId'])
    post = Post.query.get_or_404(judgeInfo['postId'])
    if user.is_collecting(post):
        message = 1
    else:
        message = 0
    response = jsonify({"collectInfo": message})
    response.status_code = 200
    return response


@api.route('/api/new_post', methods=['POST'])
@auth.login_required
def new_post():
    postInfo = request.json
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


@api.route('/api/delete_post', methods=['POST'])
@auth.login_required
def delete_post():
    postInfo = request.json
    p = Post.query.get_or_404(postInfo['postId'])
    if p is None:
        message = "the post dosen't exist"
    else:
        all_comments = Comment.query.filter_by(post_id=p.id).all()  # 删除评论
        for comment in all_comments:
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


@api.route('/api/post_category/<int:tag>', methods=['GET'])
def post_category(tag):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(goodTag=tag).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['JXNUGO_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.post_category', page=page - 1, tag=tag, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.post_category', page=page + 1, tag=tag, _external=True)
    return jsonify({'posts': [post.to_json() for post in posts],
                    'prev': prev,
                    'next': next,
                    'count': pagination.total
                    }
                   )


@api.route('/api/query_post', methods=['POST'])
def m_query_post():
    query_info=request.json
    key_word=query_info['keyWords']
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.goodName.like('%'+key_word+'%')).paginate(
        page, per_page=current_app.config['JXNUGO_POSTS_PER_PAGE'],
        error_out=False
    )
    if pagination.total is not 0:
        posts = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.query_post', page=page - 1, _external=True)
            # prev="http://www.jxnugo.com/api/posts?page=%d" % (page-1)
        next = None
        if pagination.has_next:
            # next="http://www.jxnugo.com/api/posts?page=%d" % (page+1)
            next = url_for('api.query_post', page=page + 1, _external=True)
        return jsonify({'posts': [post.to_json() for post in posts],
                    'prev': prev,
                    'next': next,
                    'count': pagination.total
                    })
    else:
        return jsonify({"message":"query_post dosen't exist"})