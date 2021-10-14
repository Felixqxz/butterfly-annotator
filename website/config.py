import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig:
    """
    set Flask configuration vars
    """
    # General config
    DEBUG = True
    TESTING = False
    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig:
    """
    config for test
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig:
    """
    set Flask configuration vars
    """
    # General config
    DEBUG = False
    TESTING = False
    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

"""
config_by_name = dict(
    test=TestConfig,
    deploy=Config
)
"""

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

