from flask import jsonify
from . import api

def forbidden(message):
    response=jsonify({'error':'forbidden','message':message})
    response.status_code=403
    return response