#-*- coding: UTF-8 -*-

from flask import Blueprint

api=Blueprint('api',__name__)

from . import views,authentication,posts,users,comments