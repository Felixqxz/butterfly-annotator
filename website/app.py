from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .database.access import db
from .config import config_by_name
from .database.loaders import setup_user_loader

# configuration
DEBUG = True

def create_app(config_name=None):
    # create and configure the app
    app = Flask(__name__)
    if config_name is None:
        app.config.from_object(config_by_name['default'])
    else:
        app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    # enable CORS
    # CORS(app, resources={r'/*': {'origins': '*'}})
    CORS(app, resources=r'/*')

    # Add routes
    from .apis.image_api import image_api
    from .apis.description_api import description_api
    app.register_blueprint(image_api)
    app.register_blueprint(description_api)

    # Create & setup LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    setup_user_loader(login_manager)

    # Add CLI custom commands
    from .cli import create_all, drop_all
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    

    # done
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
