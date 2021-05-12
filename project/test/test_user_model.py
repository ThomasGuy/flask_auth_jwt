# project/tests/test_user_model.py
import unittest
from flask_jwt_extended import create_access_token, decode_token, create_refresh_token

from project.database import db_scoped_session as db
from project.database.models import User
from project.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_decode_access_token(self):
        """ test decode access token """

        user = User(
            email='test@test.com',
            password='testpw',
            username='jonny'
        )
        db.add(user)
        db.commit()
        access_token = create_access_token(identity=user.public_id)
        refresh_token = create_refresh_token(identity=user.public_id)

        self.assertTrue(User.authenticate('testpw', username='jonny'))
        self.assertTrue(User.authenticate('testpw', email='test@test.com'))
        self.assertTrue(user.check_password('testpw'))
        self.assertTrue(decode_token(access_token)['sub'] == user.public_id)
        self.assertTrue(decode_token(refresh_token)['sub'] == user.public_id)


if __name__ == '__main__':
    unittest.main()
