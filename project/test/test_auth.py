import unittest
import json
import time
import uuid
import datetime

from flask_jwt_extended import decode_token

from project.database import db_scoped_session as db
from project.database.models import User, Blacklist
from project.test.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test - user registration """
        with self.client:
            resp_register = self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test - registration with already registered username/email """
        user = User(
            public_id=str(uuid.uuid4()),
            username='joeseph',
            email='test@gmail.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        db.add(user)
        db.commit()
        with self.client:
            response = self.register_user()
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User/email already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)
            response = self.register_user(username='wrong', email='test@gmail.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User/email already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login_username(self):
        """ Test - login of registered user with username """
        with self.client:
            # user registration
            resp_register =self.register_user( username='bobby', email='joe@gmail.com', password='12345678')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue( data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.login_user( username='bobby', email=None, password='12345678')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_user_login_email(self):
        """ Test - login of registered user with email """
        with self.client:
            # user registration
            resp_register =self.register_user( username='joeseph', email='joeyboy33@gmail.com', password='12345678')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue( data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.login_user( username=None, email='joeyboy33@gmail.com', password='12345678')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_non_registered_user_login(self):
        """ Test - login of non-registered user """
        with self.client:
            response = self.login_user(username='tom', email='twg@gmail.com', password='1989123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_incorrect_password_user_login(self):
        """ Test - login with incorrect password """
        with self.client:
            # user registration
            resp_register = self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue( data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login with wrong password
            response = self.login_user(username='joeseph', email='joe@gmail.com', password='wrongpasswd')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Password is incorrect.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
