from flask import request,jsonify, make_response, views
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    current_user,
    get_current_user
    )


class ProtectedAPI(views.MethodView):
    """ User Protected Resource """
    decorators = [jwt_required]
    def get(self):

        response_object = {
            "get current identity": get_jwt_identity(),
            "who am I?": get_current_user(),

        }
        return make_response(jsonify(response_object)), 200

