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
        post_data = request.get_json()
        try:
            # fetch the user data
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']
            user = User.query.filter(or_(User.username==username, User.email==email)).first()
            if user is not None:
                if user.check_password(password):
                    # Create/Store the tokens in store with a status of not currently revoked.
                    user_claims = app.config['JWT_IDENTITY_CLAIM']
                    auth_token = create_access_token(identity=user.id)
                    refresh_token = create_refresh_token(identity=user.id)
                    add_token_to_database(auth_token, user_claims)
                    add_token_to_database(refresh_token, user_claims)
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token,
                        'refresh_token': refresh_token
                    }
                    return make_response(jsonify(responseObject)), 201
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Password is incorrect.'
                    }
                    return make_response(jsonify(responseObject)), 401
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 401
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500
