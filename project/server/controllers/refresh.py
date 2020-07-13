from flask import jsonify, make_response, views
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token
    )

from project.server.util.blacklist_helpers import add_token_to_database

class RefreshToken(views.MethodView):
    """ refresh access token """
    decorators = [jwt_refresh_token_required]
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        add_token_to_database(access_token)

        responseObject = {
            'access_token': access_token
        }
        return make_response(jsonify(responseObject)), 200
