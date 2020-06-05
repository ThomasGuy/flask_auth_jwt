from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


from project.database import init_db, db_scoped_session as db

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)
    bcrypt.init_app(app)
    engine = init_db(app.config.get('SQLALCHEMY_DATABASE_URI'))

    with app.app_context():
        from project.server.controllers import auth_blueprint
        app.register_blueprint(auth_blueprint)


        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db.remove()

    return app, engine
