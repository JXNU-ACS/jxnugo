from flask import jsonify,g
from flask.ext.httpauth import HTTPBasicAuth
from errors import forbidden

auth=HTTPBasicAuth()

@auth.verify_password
def verify_password(username,useremail):
    if username=='':
        g.current_user=AnonymousUser()
        return True
    user=User.query.filter_by(userName=username).first()
    if not user:
        return False
    g.current_user=user
    return user.verify_password(passWord)