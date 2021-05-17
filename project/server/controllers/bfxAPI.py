""" Bitfinex API """
from dataclasses import asdict

from flask import request, jsonify, make_response, views

from ..bitfinex.bfx import vault


class BfxAPI(views.MethodView):
    """/api/tickers"""

    def get(self):
        """get all tickers"""
        tickerData = []
        for ticker in vault.values():
            tickerData.append(asdict(ticker))

        if tickerData:
            response = {"status": "success", "data": tickerData}
            return make_response(jsonify(response)), 200

        response = {"status": "fail", "message": "Server error"}
        return make_response(jsonify(response)), 500

    def post(self):
        """
        return a list of tickers from request
        :params: post data list of symbols
        :return: response
        """
        post_data = request.get_json()
        tickers = []
        for symbol in post_data:
            tickers.append(vault[symbol])

        if tickers:
            response = {"status": "success", "data": tickers}

            return make_response(jsonify(response)), 200

        response = {"status": "fail", "message": "No such ticker"}
        return make_response(jsonify(response)), 500
