""" User Registration Resource """

from flask import request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import or_
from flask_jwt_extended import create_access_token

from project.database.models import User
from project.database import db_scoped_session as db
from project.server.util.blacklist_helpers import add_token_to_database


class RegisterAPI(MethodView):
    """/auth/register"""

    def post(self):
        """process user registration"""
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter(
            or_(
                User.username == post_data.get("username"),
                User.email == post_data.get("email"),
            )
        ).first()
        if user is None:
            try:
                user = User(
                    username=post_data.get("username"),
                    email=post_data.get("email"),
                    password=post_data.get("password"),
                )

                # insert the user
                db.add(user)
                db.commit()
                # generate the auth token
                access_token = create_access_token(identity=user.public_id)
                add_token_to_database(access_token)
                responseObject = {"status": "success", "access_token": access_token}
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    "status": "fail",
                    "message": "Some error occurred. Please try again.",
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "User/email already exists. Please Log in.",
            }
            return make_response(jsonify(responseObject)), 202
