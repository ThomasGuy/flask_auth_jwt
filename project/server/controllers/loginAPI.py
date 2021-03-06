from flask import request, make_response, jsonify
from flask import current_app as app
from flask.views import MethodView
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, create_refresh_token

from project.server.util.blacklist_helpers import add_token_to_database
from project.database.models import User


class LoginAPI(MethodView):
    """ User Login Resource """
    def post(self):
        # get the post data
        credentials = request.get_json()
        try:
            user = User.authenticate(**credentials)
            if user:
                # user_claims = app.config['JWT_IDENTITY_CLAIM'] or None
                access_token = create_access_token(identity=user.public_id)
                refresh_token = create_refresh_token(identity=user.public_id)
                add_token_to_database(access_token)
                add_token_to_database(refresh_token)
                responseObject = {
                    'status': 'success',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
                return make_response(jsonify(responseObject)), 201

            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 202
        except Exception as e:

            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500
