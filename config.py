import os
import datetime

from dotenv import load_dotenv
load_dotenv()

postgres_local_base = os.environ['DB_DATABASE']
db_name = 'jwt_auth'


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'my_precious_secret_key')
    JWT_IDENTITY_CLAIMS = ''


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + db_name


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + db_name + '_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgres_local_base + db_name


config_name = {
    'dev' : 'DevelopmentConfig',
    'test': 'TestingConfig',
    'prod': 'ProductionConfig'
}

jwt_key = Config.JWT_SECRET_KEY