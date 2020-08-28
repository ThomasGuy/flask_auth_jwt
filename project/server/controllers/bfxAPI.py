from dataclasses import asdict

from flask import request,jsonify, make_response, views
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    current_user,
    get_current_user
    )

from ..bitfinex.bfx import vault


class BfxAPI(views.MethodView):
    """ Bitfinex API """
    # decorators = [jwt_required]

    def get(self):
        tickerData = []
        for ticker in vault.values():
            tickerData.append(asdict(ticker))

        if tickerData:
            response = {
                'status': 'success',
                'data': tickerData
            }

            return make_response(jsonify(response)), 200

        else:
            response = {
                'status': 'fail',
                'message': 'Server error'
            }

            return make_response(jsonify(response)), 500

    def post(self):
        post_data = request.get_json()
        ticker = vault[post_data['data']]

        if ticker:
            response = {
                'status': 'success',
                'data': asdict(ticker)
            }

            return make_response(jsonify(response)), 200

        else:
            response = {
                'status': 'fail',
                'message': 'No such ticker'
            }

            return make_response(jsonify(response)), 500
