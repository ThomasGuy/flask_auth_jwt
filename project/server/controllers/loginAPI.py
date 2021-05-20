"""User Login Resource"""
from flask import request, make_response, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token

from project.server.util.blacklist_helpers import add_token_to_database
from project.database.models import User


class LoginAPI(MethodView):
    """ auth/login """

    def post(self):
        """validate user login"""
        # get the post data
        credentials = request.get_json()
        try:
            user = User.authenticate(**credentials)
            if user:
                access_token = create_access_token(identity=user.public_id)
                refresh_token = create_refresh_token(identity=user.public_id)
                add_token_to_database(access_token)
                add_token_to_database(refresh_token)
                responseObject = {
                    "status": "success",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                return make_response(jsonify(responseObject)), 201

            responseObject = {"status": "fail", "message": "User does not exist."}
            return make_response(jsonify(responseObject)), 202

        except Exception:
            responseObject = {"status": "fail", "message": "Try again"}
            return make_response(jsonify(responseObject)), 500
