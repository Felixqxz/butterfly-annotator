import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Represents different configurations of the app.
    """
    def __init__(self, debug, testing, sql_alchemy_track_modifications, sql_alchemy_database_uri = 'sqlite:///test.db'):
        """
        :param debug: Debug mode (boolean)
        :param testing: Testing mode (boolean)
        :param sql_alchemy_track_modifications: Enables SQLAlchemy to track modifications on the database (boolean)
        :param sql_alchemy_database_uri: The URI towards the database (string)
        """
        assert type(debug) == bool
        assert type(testing) == bool
        assert type(sql_alchemy_track_modifications) == bool
        assert type(sql_alchemy_database_uri) == str

        self.debug = debug
        self.testing = testing
        self.sql_alchemy_database_uri = sql_alchemy_database_uri
        self.sql_alchemy_track_modifications = sql_alchemy_track_modifications

config_by_name = {
    "development": Config(debug = True, testing = False, sql_alchemy_track_modifications = True),
    "testing": Config(debug = True, testing = True, sql_alchemy_track_modifications = True),
    "production": Config(debug = False, testing = False, sql_alchemy_track_modifications = False),
    "default": Config(debug = True, testing = False, sql_alchemy_track_modifications = True)
}
