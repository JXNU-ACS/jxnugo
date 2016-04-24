#-*- coding: UTF-8 -*-
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'),500

@main.app_errorhandler(403)
def request_error(e):
    return render_template('403.html'),403