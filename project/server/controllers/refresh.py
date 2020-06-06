from flask import jsonify, make_response, views
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token
    )

class RefreshToken(views.MethodView):
    """ refresh access token """
    decorators = [jwt_refresh_token_required]
    def post(self):
        current_user = get_jwt_identity()
        response = {
            'access_token': create_access_token(identity=current_user)
        }
        return make_response(jsonify(response)), 200
