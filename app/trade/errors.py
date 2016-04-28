#-*- coding: UTF-8 -*-
from flask import render_template
from . import trade

@trade.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@trade.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'),500