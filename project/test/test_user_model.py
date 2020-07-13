# project/tests/test_user_model.py
import uuid
import unittest
import datetime

from flask_jwt_extended import create_access_token, decode_token

from project.database import db_scoped_session as db
from project.database.models import User
from project.test.base import BaseTestCase

class TestUserModel(BaseTestCase):

    def test_decode_access_token(self):
        """ test decode access token """
        public_id=str(uuid.uuid4())
        user = User(
            public_id=public_id,
            email='test@test.com',
            password='testpw',
            username='jonny',
            registered_on=datetime.datetime.utcnow()
        )
        db.add(user)
        db.commit()
        access_token = create_access_token(identity=user.public_id)
        self.assertTrue(User.authenticate( 'testpw', public_id=public_id))
        self.assertTrue(User.authenticate( 'testpw', username='jonny'))
        self.assertTrue(User.authenticate( 'testpw', email='test@test.com'))
        self.assertTrue(user.check_password('testpw'))
        self.assertTrue(decode_token(access_token)) == user.username


if __name__ == '__main__':
    unittest.main()
