''' Logout user '''
from flask import jsonify, make_response, views
from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from project.database.models import Blacklist
from project.database import db_scoped_session


class LogoutAPI(views.MethodView):
    """ /auth/logout """
    decorators = [jwt_required]

    def get(self):
        ''' Logout '''
        jti = get_jwt()['jti']
        try:
            token = Blacklist.query.filter_by(jti=jti).first()
            token.revoked = True
            db_scoped_session.commit()
            responseObject = {
                'status': 'success',
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': e.message
            }
            return make_response(jsonify(responseObject)), 500
