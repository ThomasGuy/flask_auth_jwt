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
            response = self.client.post(
                '/api/tickers',
                headers=dict(Authorization='Bearer ' + 'secret'),
                data=json.dumps(dict(
                    coin='BTC'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            for ticker in data['data']:
                print(ticker['symbol'], ticker['last_price'])
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(len(data['data']) > 0)

