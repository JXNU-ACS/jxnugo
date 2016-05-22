# -*- coding: UTF-8 -*-
from flask import jsonify
from . import api
from ..exceptions import ValidationError


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def methodNotAllowed(message):
    response = jsonify({'error': 'method Not Allowed','message':message})
    response.status_code = 405
    return response


def ResourceConflict(message):
    response = jsonify({'error': 'Resource Conflict' , 'message': message})
    response.status_code = 409
    return response



def NotAccept(message):
    response = jsonify({'error' : 'upload message error', 'message':message})
    response.status_code = 406
    return response



@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

