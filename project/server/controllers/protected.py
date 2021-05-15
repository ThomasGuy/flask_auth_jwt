import logging

from flask import request, jsonify, make_response, views
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    current_user,
    get_current_user,
)

log = logging.getLogger(__name__)


class ProtectedAPI(views.MethodView):
    """User Protected Resource"""

    @jwt_required()
    def get(self):
        try:
            response_object = {
                "status": "success",
                "userId": get_jwt_identity(),
                "current_user": get_current_user(),
            }
            return make_response(jsonify(response_object)), 200
        except Exception as err:
            response_object = {"status": "fail", "message": err}
            return make_response(jsonify(response_object)), 500
