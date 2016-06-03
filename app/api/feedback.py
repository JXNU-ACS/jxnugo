# -*- coding: UTF-8 -*-
from flask import jsonify, request, g, abort, current_app
from ..email import send_email
from . import api


@api.route('/api/feedback', methods=['POST'])
def feedback():
    feedbackInfo = request.json
    if feedbackInfo['Body'] is not None:
        send_email(current_app.config['JXNU_PLUS_MAIL'], '意见反馈',
                   'auth/email/feedback', Body=feedbackInfo['Body'], Email=feedbackInfo['Email'], Respondent=feedbackInfo['Respondent']
                   )
        response=jsonify({"feedbackInfo":"successful"})
        response.code_status=200
        return response


@api.route('/api/get_notice')
def get_notice():
    f = open('notice.txt', 'r')
    content = f.read()
    response = jsonify({'notice': content})
    response.code_status = 200
    return response