# -*- coding: UTF-8 -*-
from flask import jsonify, current_app, url_for, request, g
from ..models import getPrimaryKeyId, JxnuTour
from . import api
from .. import db
from .errors import bad_request


@api.route('/api/tour/search_location', methods=['POST'])
def search_locaton():
    search_info=request.json
    car = JxnuTour.query.filter_by(car_id = search_info['car_id']).first()
    response=jsonify({"latitude":car.car_x, "longitudes":car.car_y, "angle":car.car_angle})
    response.status_code = 200
    return response


@api.route('/api/tour/update_location', methods=['POST'])
def update_location():
    update_info = request.json
    car = JxnuTour(car_id = update_info['car_id'], car_x = update_info['car_latitude'],
                   car_y = update_info['car_longitudes'], car_angle = update_info['car_angle'])
    db.session.add(car)
    db.session.commit()
    response=jsonify({"update_info":"successful"})
    response.status_code = 200
    return response