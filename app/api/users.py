# -*- coding: UTF-8 -*-
from flask import jsonify
from authentication import auth
from ..models import User
from . import api

@api.route('/api/user/<int:id>')
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
    followers=user.followers
    return jsonify({"followers":[follower.to.json] for follower in followers})