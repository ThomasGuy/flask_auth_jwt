import os
import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

db_name = 'jwt_auth'
local_sqldb = 'sqlite:///' + str(Path.cwd()) +'/'
postgres_local_base = os.getenv('PG_LOCAL', local_sqldb)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'my_precious_secret_key')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ERROR_MESSAGE_KEY = 'message'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + db_name
    JWT_ACCESS_TOKEN_EXPIRES = 3*60
    JWT_REFRESH_TOKEN_EXPIRES = 3600*6 # seconds

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + db_name + '_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = 5 # seconds
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=2) # seconds


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgres_local_base + db_name
    FLASK_ENV='production'
    JWT_ACCESS_TOKEN_EXPIRES = 15*60 # seconds
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=3000) # seconds


config_name = {
    'dev' : 'DevelopmentConfig',
    'test': 'TestingConfig',
    'prod': 'ProductionConfig'
}

jwt_key = Config.JWT_SECRET_KEY
