import json
import datetime
import uuid

from flask_testing import TestCase
from flask import current_app as app

from project.database import db_scoped_session, init_db, Base


class BaseTestCase(TestCase):
    """ Base Test """

    engine = None

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        self.engine = init_db(app.config['SQLALCHEMY_DATABASE_URI'])

    def tearDown(self):
        db_scoped_session.remove()
        Base.metadata.drop_all(self.engine)

    # # helpers
    # def register_user(self, username='joeseph', email='joe@gmail.com', password='123456', public_id=None):
    #     """ register test user post request  """
    #     return self.client.post(
    #         '/auth/register',
    #         data=json.dumps(dict(
    #             public_id=public_id,
    #             username=username,
    #             email=email,
    #             password=password,
    #             registered_on=datetime.datetime.utcnow()
    #         )),
    #         content_type='application/json'
    #     )

    # def login_user(self, username, email, password, public_id=None):
    #     """ login test user post request """
    #     return self.client.post(
    #         '/auth/login',
    #         data=json.dumps(dict(
    #             public_id=public_id,
    #             username=username,
    #             email=email,
    #             password=password,
    #             registered_on=datetime.datetime.utcnow()
    #         )),
    #         content_type='application/json'
    #     )
