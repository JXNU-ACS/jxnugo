#-*- coding: UTF-8 -*-
from flask import g, jsonify,current_app
from flask.ext.httpauth import HTTPBasicAuth
from ..models import User, AnonymousUser
from . import api
from .errors import unauthorized, forbidden
from qiniu import Auth,put_file,etag,urlsafe_base64_encode
import qiniu.config
from uuid import uuid4

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    if username_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(username_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(userName=username_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_passWord(password)


@auth.error_handler
def auth_error():
    return unauthorized(u'凭证无效')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden(u'账户未激活或未登陆')


@api.route('/api/get_token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized(u'凭证无效')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})


@api.route('/api/get_mobile_token',methods=['GET'])
def get_mobile_token():
    q=Auth(current_app.config['QINIU_ACCESS_KEY'],current_app.config['QINIU_SECRET_KEY'])
    bucket_name='trade'
    policy={
         "scope": "trade"
    }
    key=None
    mobile_upload_token=q.upload_token(bucket_name,key,3600,policy)
    return jsonify({'uptoken':mobile_upload_token})


@api.route('/api/get_mobile_key',methods=['GET'])
def get_mobile_key():
    key=uuid4()
    return jsonify({'upkey':key})


@api.route('/api/get_upload_token',methods=['GET'])
def get_upload_token():
    q=Auth(current_app.config['QINIU_ACCESS_KEY'],current_app.config['QINIU_SECRET_KEY'])
    bucket_name='trade'
    key=uuid4()
    policy={
         "scope": "trade"
    }
    uptoken=q.upload_token(bucket_name,key,3600,policy)
    return jsonify({'uptoken':uptoken,'key':key})