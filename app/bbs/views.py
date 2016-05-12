# -*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,session,flash
from ..decorators import admin_required,permission_required
from . import bbs
from .. import db
from flask.ext.login import login_required,current_user
from ..models import Permission,User,Role,Post

@bbs.route('/bbs_index')
def bbs_index():
    flash(u'校园bbs界面开发中')
    return render_template('trade/trade_list.html')