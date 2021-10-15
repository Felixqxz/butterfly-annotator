import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Represents different configurations of the app.
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestConfig(Config):
    Testing = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_by_name = {
    'development': Config,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': Config
}
