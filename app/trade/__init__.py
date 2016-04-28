#-*- coding: UTF-8 -*-
from flask import Blueprint

trade=Blueprint('trade',__name__)
from . import errors,views
