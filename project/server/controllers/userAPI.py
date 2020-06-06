from flask import jsonify, make_response, views, request
from flask_jwt_extended import (
    jwt_required,
    get_current_user,
    current_user
    )


class UserAPI(views.MethodView):
    """ User Protected Resource """
    decorators = [jwt_required]
    def post(self):
        # get the post data
        post_data = request.get_json()
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''

        if auth_token:
            responseObject = {
                'status': 'success',
                'message': 'You are authorized.',
                'get_current_user': get_current_user()
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
