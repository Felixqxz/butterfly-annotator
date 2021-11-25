import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Represents different configurations of the app.
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///butterfly.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'super secret key'
    SESSION_TYPE = 'annonation'
    REMEMBER_COOKIE_DURATION = timedelta(days = 1)

class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'super secret key'
    SESSION_TYPE = 'annonation'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super secret key'
    SESSION_TYPE = 'annonation'

config_by_name = {
    'development': Config,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': Config
}
