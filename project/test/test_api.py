import json
import time

from project.test.base import BaseTestCase
from project.server.util.blacklist_helpers import is_token_revoked


class TestApiBlueprint(BaseTestCase):
    def test_tickers(self):
        """test - Tickers api"""
        time.sleep(5)
        with self.client:
            # user registration
            resp_register = self.register_user(
                username="joeseph", email="joeyboy33@gmail.com", password="12345678"
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register["status"] == "success")
            self.assertTrue(data_register["access_token"])
            self.assertTrue(resp_register.content_type == "application/json")
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.login_user(
                username=None, email="joeyboy33@gmail.com", password="12345678"
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["access_token"])
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 201)

            api_response = self.client.get(
                "/api/tickers",
                headers=dict(Authorization="Bearer " + data["access_token"]),
                # data=json.dumps(dict(
                #     coin='BTC'
                # )),
                content_type="application/json",
            )
            data = json.loads(api_response.data.decode())
            self.assertTrue(data["status"] == "success")
            if data["status"] == "success":
                for ticker in data["data"]:
                    print(ticker["symbol"], ticker["last_price"])
            else:
                print("data server fail")
            self.assertTrue(len(data["data"]) > 0)
