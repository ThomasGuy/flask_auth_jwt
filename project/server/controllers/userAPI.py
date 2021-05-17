""" User Protected Resource '/auth/status' """

from flask import jsonify, make_response, views, request
from flask_jwt_extended import jwt_required, current_user


class UserAPI(views.MethodView):
    """serve user data"""

    @jwt_required()
    def post(self):
        """get the post data then do something with it"""
        post_data = request.get_json()
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                access_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    "status": "fail",
                    "message": "Bearer token malformed.",
                }
                return make_response(jsonify(responseObject)), 401
        else:
            access_token = ""

        if access_token:
            responseObject = {
                "status": "success",
                "current_user": current_user,
                "name": current_user.get("username"),
                "data": f"we got your {post_data}",
            }
            return make_response(jsonify(responseObject)), 200

        responseObject = {
            "status": "fail",
            "message": "Provide a valid auth token.",
        }
        return make_response(jsonify(responseObject)), 401
