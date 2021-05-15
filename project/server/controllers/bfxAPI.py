""" Bitfinex API """
from dataclasses import asdict

from flask import request, jsonify, make_response, views
from flask_jwt_extended import jwt_required, current_user

from ..bitfinex.bfx import vault


class BfxAPI(views.MethodView):
    """/api/tickers"""

    @jwt_required()
    def get(self):
        """get all tickers"""
        tickerData = []
        for ticker in vault.values():
            tickerData.append(asdict(ticker))

        if tickerData:
            response = {"status": "success", "data": tickerData}

            return make_response(jsonify(response)), 200

        else:
            response = {"status": "fail", "message": "Server error"}

            return make_response(jsonify(response)), 500

    def post(self):
        """get ticker[symbol]"""
        post_data = request.get_json()
        ticker = vault[post_data["data"]]

        if ticker:
            response = {"status": "success", "data": asdict(ticker)}

            return make_response(jsonify(response)), 200

        else:
            response = {"status": "fail", "message": "No such ticker"}

            return make_response(jsonify(response)), 500
