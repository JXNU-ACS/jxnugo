#-*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,session

from . import main
from .. import db


@main.route('/trade_list')
def trade_list():
    return render_template('trade_list.html')

@main.route('/trade_detail')
def trade_detail():
    return render_template("trade_detail.html")

@main.route('/trade_post')
def trade_post():
    return render_template("trade_post")

@main.route('/user_zone')
def user_zone():
    return render_template("user_zone.html")