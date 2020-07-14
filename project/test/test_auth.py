import unittest
import json
import time
import uuid
import datetime

from flask_jwt_extended import decode_token, get_jwt_identity

from project.database import db_scoped_session as db
from project.database.models import User, Blacklist
from project.test.base import BaseTestCase
from project.server.util.blacklist_helpers import is_token_revoked


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test - user registration """
        with self.client:
            resp_register = self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            self.assertFalse(is_token_revoked(decode_token(data_register['access_token'])))

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
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.login_user( username='bobby', email=None, password='12345678')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['access_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_user_login_email(self):
        """ Test - login of registered user with email """
        with self.client:
            # user registration
            resp_register =self.register_user( username='joeseph', email='joeyboy33@gmail.com', password='12345678')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.login_user( username=None, email='joeyboy33@gmail.com', password='12345678')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['access_token'])
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
            self.assertEqual(response.status_code, 202)

    def test_incorrect_password_user_login(self):
        """ Test - login with incorrect password """
        with self.client:
            # user registration
            resp_register = self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login with wrong password
            response = self.login_user(username='joeseph', email='joe@gmail.com', password='wrongpasswd')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_valid_logout(self):
        """ Test - logout before token expires """
        with self.client:
            # user registration
            resp_register =self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.login_user(username='joeseph', email='joe@gmail.com', password='123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['access_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 201)
            # valid token logout
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + data_login['access_token']
                )
            )
            data = json.loads(response.data.decode())
            # print(f'data: {data}')
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """ Test - logout after the token expires """
        with self.client:
            # user registration
            resp_register = self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.login_user(username='joeseph', email='joe@gmail.com', password='123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['access_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 201)
            # invalid token logout
            time.sleep(6)
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + data_login['access_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['sub_status'] == 42)
            self.assertTrue(data['message'] == 'The access token has expired')
            self.assertEqual(response.status_code, 401)

    def test_refresh_expired_token(self):
        """ Test - refresh expired token and access protected endpoint """
        with self.client:
            # user registration
            resp_register = self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['access_token'])
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.login_user(username='joeseph', email='joe@gmail.com', password='123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['access_token'])
            self.assertTrue(data_login['refresh_token'])
            self.assertEqual(resp_login.status_code, 201)
            # invalid token
            time.sleep(6)
            response = self.client.get(
                '/protected',
                headers=dict(
                    Authorization='Bearer ' + data_login['access_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['sub_status'] == 42)
            self.assertTrue(data['message'] == 'The access token has expired')
            self.assertEqual(response.status_code, 401)
            # get refresh access token
            refresh_response = self.client.get(
                '/auth/refresh',
                headers=dict(
                    Authorization='Bearer ' + data_login['refresh_token']
                )
            )
            data_refresh = json.loads(refresh_response.data.decode())
            self.assertTrue(data_refresh['access_token'])
            self.assertFalse(is_token_revoked(decode_token(data_refresh['access_token'])))
            response = self.client.get(
                '/protected',
                headers=dict(
                    Authorization='Bearer ' + data_refresh['access_token']
                )
            )
            data_final = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)


    def test_user_status(self):
        """ Test - user status """
        with self.client:
            resp_register = self.register_user(username='Thomas', email='tom@mail.box', password='ahoy')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            resp_login = self.login_user(username='Thomas', email='', password='ahoy')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['access_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 201)
            response = self.client.post(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + data_login['access_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data is not None)
            self.assertTrue(isinstance(data['get_current_user'], dict))
            # self.assertTrue(data['current_user']['admin'] == 'true' or 'false')
            self.assertEqual(response.status_code, 200)
            print(f'get_current_user {data["get_current_user"]}')
            print('token identity: ', decode_token(data_login['access_token'])['identity'])

    def test_using_revoked_access_token(self):
        """ Test - using revoked access token """
        with self.client:
            # user registration
            resp_register = self.register_user(username='Tom')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.login_user(username='Tom', email=None, password='123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['access_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 201)
            jti = decode_token(data_login['access_token'])['jti']
            token = Blacklist.query.filter_by(jti=jti).first()
            token.revoked = True
            db.commit()
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + data_login['access_token']
                )
            )
            data = json.loads(response.data.decode())
            print('data: ', data)
            self.assertTrue(data['message'] == 'Token has been revoked')


    def test_valid_blacklisted_token_logout(self):
        """ Test - logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            resp_register = self.register_user()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['access_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.login_user(username='joeseph', email='joe@gmail.com', password='123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['access_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            # self.assertEqual(resp_login.status_code, 200)
            # blacklist a valid token
            jti = decode_token(data_login['access_token'])['jti']
            token = Blacklist.query.filter_by(jti=jti).first()
            token.revoked = True
            db.commit()
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + data_login['access_token']
                )
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertTrue(data['message'] == 'Token has been revoked')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
