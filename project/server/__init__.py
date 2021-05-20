""" Initialize apllication """
import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from project.database import init_db, db_scoped_session, _bcrypt
from project.server.util.blacklist_helpers import is_token_revoked
from project.server.services.events import sockio
from project.database.models import Blocklist, User

log = logging.getLogger(__name__)
jwt = JWTManager()


def create_app(Config):
    """application factory
    params: <config>
    return app engine
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)
    _bcrypt.init_app(app)
    engine = init_db(app.config.get("SQLALCHEMY_DATABASE_URI"))
    CORS(app)
    sockio.init_app(app, manage_session=False)

    with app.app_context():
        # pylint: disable=unused-variable, import-outside-toplevel
        from project.server.controllers import auth_blueprint, api_blueprint

        app.register_blueprint(auth_blueprint)
        app.register_blueprint(api_blueprint)

        # Using the expired_token_loader decorator, we will now call
        # this function whenever an expired but otherwise valid access
        # token attempts to access an endpoint
        @jwt.expired_token_loader
        def my_expired_token_callback(jwt_header, jwt_data):
            token_type = jwt_data["type"]
            return (
                jsonify(
                    {
                        "status": 401,
                        "sub_status": 42,
                        "token_type": token_type,
                        "message": "The {} token has expired".format(token_type),
                    }
                ),
                401,
            )

        # Define our callback function to check if a token has been revoked or not
        @jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload):
            return is_token_revoked(jwt_payload)

        @jwt.user_lookup_loader
        def user_loader_callback(_jwt_header, jwt_data):
            identity = jwt_data["sub"]
            log.info(f"current_user {User.query.filter_by(public_id=identity).all()}")
            return User.query.filter(User.public_id == identity).first()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_scoped_session.remove()

    return app, engine
