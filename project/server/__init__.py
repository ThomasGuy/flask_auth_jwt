from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from project.database import init_db, db_scoped_session as db
from project.server.util.blacklist_helpers import is_token_revoked

jwt = JWTManager()
flask_bcrypt = Bcrypt()


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)
    flask_bcrypt.init_app(app)
    engine = init_db(app.config.get('SQLALCHEMY_DATABASE_URI'))

    with app.app_context():
        from project.server.controllers import auth_blueprint
        app.register_blueprint(auth_blueprint)

        # Using the expired_token_loader decorator, we will now call
        # this function whenever an expired but otherwise valid access
        # token attempts to access an endpoint
        @jwt.expired_token_loader
        def my_expired_token_callback(expired_token):
            token_type = expired_token['type']
            return jsonify({
                'status': 401,
                'sub_status': 42,
                'token_type': token_type,
                'msg': 'The {} token has expired'.format(token_type)
            }), 401

        # Define our callback function to check if a token has been revoked or not
        @jwt.token_in_blacklist_loader
        def check_if_token_revoked(decoded_token):
            return is_token_revoked(decoded_token)

        @jwt.user_loader_callback_loader
        def user_loader_callback(identity):
            from project.database.models import User
            user = User.query.filter(User.public_id==identity).first()
            if user is None:
                return None
            else:
                return user.username

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db.remove()

    return app, engine

import project.database.models
