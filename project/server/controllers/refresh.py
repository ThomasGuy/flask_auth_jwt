from flask import jsonify, make_response, views
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token
    )

class RefreshToken(views.MethodView):
    """ refresh access token """
    decorators = [jwt_refresh_token_required]
    def get(self):
        user_id = get_jwt_identity()
        response = {
            'access_token': create_access_token(identity=user_id)
        }
        # return make_response(jsonify(response)), 200
        return jsonify(response), 200
