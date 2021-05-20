""" Logout user """
import logging
from flask import jsonify, make_response, views
from flask_jwt_extended import jwt_required, get_jwt

from project.database.models import Blocklist
from project.database import db_scoped_session

log = logging.getLogger(__name__)


class LogoutAPI(views.MethodView):
    """/auth/logout"""

    @jwt_required()
    def get(self):
        """Logout"""
        # auth_header = request.headers.get("Authorization")
        jti = get_jwt()["jti"]
        try:
            token = Blocklist.query.filter_by(jti=jti).first()
            token.revoked = True
            db_scoped_session.commit()
            responseObject = {
                "status": "success",
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {"status": "fail", "message": e.message}
            log.info(f"lougout fail: {e.message}")
            return make_response(jsonify(responseObject)), 500
