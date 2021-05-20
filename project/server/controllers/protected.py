"""User Protected Resource"""
import logging
from flask import jsonify, make_response, views
from flask_jwt_extended import (
    jwt_required,
    current_user,
)

log = logging.getLogger(__name__)


class ProtectedAPI(views.MethodView):
    """ /protected """

    @jwt_required()
    def get(self):
        """ test current user returned on protected endpoint """
        try:
            response_object = {
                "status": "success",
                "current_user": current_user,
            }
            return make_response(jsonify(response_object)), 200

        except Exception as err:
            response_object = {"status": "fail", "message": err}
            log.info("protected api error, auth?")
            return make_response(jsonify(response_object)), 500
