import os
import unittest

from flask import current_app as app
from flask_testing import TestCase


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious_secret_key')
        self.assertFalse(app.config['JWT_SECRET_KEY'] == 'my_precious_secret_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres+psycopg2://bella20:61512@localhost:5433/jwt_auth'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious_secret_key')
        self.assertFalse(app.config['JWT_SECRET_KEY'] == 'my_precious_secret_key')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres+psycopg2://bella20:61512@localhost:5433/jwt_auth_test'
        )



class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
