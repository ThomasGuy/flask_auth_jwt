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
                access_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            access_token = ''

        if access_token:
            responseObject = {
                'status': 'success',
                'get_current_user': get_current_user(),
                'name': current_user.get('username')
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
