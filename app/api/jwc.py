# -*- coding: UTF-8 -*-
from flask import jsonify, current_app, url_for, request, g
from ..models import getPrimaryKeyId, JxnuTour
from . import api
from .. import db
from .errors import bad_request
from ..jxnuspider.jwcspider import JwcSpider


@api.route('/api/stu_info')
def get_stu_info():
    stu = JwcSpider()
    stu.get_cookie()
    stu_response = stu.get_stu_info()
    return jsonify(stu_response)


@api.route('/api/stu_grade')
def get_stu_grade():
    stu = JwcSpider()
    stu.get_cookie()
    stu_response = stu.get_stu_grade()
    return jsonify(stu_response)


@api.route('/api/stu_timetable' )
def get_stu_timetable():
    stu = JwcSpider()
    stu.get_cookie()
    stu_response = stu.get_stu_timetable()
    return jsonify(stu_response)


@api.route('/api/exam_schedule')
def get_exam_schedule():
    stu = JwcSpider()
    stu.get_cookie()
    stu_response = stu.get_stu_exam_schedule()
    return jsonify(stu_response)


@api.route('/api/is_jxnu_student', methods=['POST'])
def is_jxnu_student():
    stu = JwcSpider()
    info = request.json
    student_id = info['student_id']
    stu.get_cookie()
    jwc_name = stu.is_jxnu_student(student_id)
    return jsonify({"student_name": jwc_name})

