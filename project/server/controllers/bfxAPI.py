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
    decorators = [jwt_required]
    def get(self):
        tickerData = []
        for ticker in vault:
            tickerData.append(asdict(ticker))

        return make_response(jsonify(tickerData)), 200
