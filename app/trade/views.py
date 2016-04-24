#-*- coding: UTF-8 -*-
from flask import render_template,redirect,url_for,session

from . import trade
from .. import db


@trade.route('/trade_list')
def trade_list():
    return render_template('trade/trade_list.html')

@trade.route('/trade_detail')
def trade_detail():
    return render_template("trade/trade_detail.html")

@trade.route('/trade_post')
def trade_post():
    return render_template("trade/trade_post.html")
