""" project configuration """
from datetime import datetime, timedelta
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = "jwt_auth"
LOCAL_SQLITE_DB = "sqlite:///" + str(Path.cwd()) + "/"
postgres_local_base = os.getenv("PG_LOCAL", LOCAL_SQLITE_DB)


class Config:
    """ Base config """

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_precious_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ERROR_MESSAGE_KEY = "message"


class DevelopmentConfig(Config):
    """ Dev config """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + DB_NAME
    JWT_ACCESS_TOKEN_EXPIRES = 15 * 60
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=2)  # seconds


class TestingConfig(Config):
    """ test config """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + DB_NAME + "_test"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = 5  # seconds
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=2)


class ProductionConfig(Config):
    """ production config """

    SQLALCHEMY_DATABASE_URI = postgres_local_base + DB_NAME
    FLASK_ENV = "production"
    JWT_ACCESS_TOKEN_EXPIRES = 15 * 60  # seconds
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=3000)  # seconds


config_name = {
    "dev": "DevelopmentConfig",
    "test": "TestingConfig",
    "prod": "ProductionConfig",
}

jwt_key = Config.JWT_SECRET_KEY
