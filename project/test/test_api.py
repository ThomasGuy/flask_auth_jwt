import unittest
import json
import time
import uuid
import datetime

from flask_jwt_extended import decode_token

from project.database import db_scoped_session as db
from project.database.models import User, Blacklist
from project.test.base import BaseTestCase


class TestApiBlueprint(BaseTestCase):

    def test_tickers(self):
        """ test - Tickers api """
        time.sleep(5)
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

            api_response = self.client.get(
                '/api/tickers',
                headers=dict(Authorization='Bearer ' + data['access_token']),
                # data=json.dumps(dict(
                #     coin='BTC'
                # )),
                content_type='application/json'
            )
            data = json.loads(api_response.data.decode())
            for ticker in data['data']:
                print(ticker['symbol'], ticker['last_price'])
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(len(data['data']) > 0)

