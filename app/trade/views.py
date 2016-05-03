#-*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,session,flash,request,current_app
from ..decorators import admin_required,permission_required
from . import trade
from .. import db
from flask.ext.login import login_required,current_user
from ..models import Permission,User,Role,Post
from forms import PostForm

@trade.route('/trade_list')
def trade_list():
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['JXNUGO_POSTS_PER_PAGE'],
        error_out=False)
    posts=pagination.items
    return render_template('trade/trade_list.html',posts=posts,pagination=pagination)



@trade.route('/trade_post',methods=['POST','GET'])
@login_required
def trade_post():
    form=PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post=Post(id=form.formId.data,body=form.body.data,goodName=form.name.data,goodPrice=form.price.data,goodNum=form.num.data,
                  goodLocation=form.location.data,goodQuality=form.quality.data,goodTag=form.tag.data,
                  goodBuyTime=form.buyTime.data,contact=form.mycontact.data,
                  author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash(u'帖子发布成功')
        return redirect(url_for('main.index'))
    return render_template('trade/trade_post.html',form=form)


@trade.route('/trade_detail/<id>')
def post(id):
    post=Post.query.get_or_404(id)
    return render_template('trade/trade_detail.html',post=post)

