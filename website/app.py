from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
import os

from .config import config_by_name
from .database.access import db
from .database.models import User
from .images.discovery import discover_all_banks

# configuration
DEBUG = True
config_name = 'default'


def create_super_user():
    find = db.session.query(User).filter(User.username == 'admin').first()
    if find is None:
        password = 'admin'
        if os.path.isfile('password.txt'):
            with open('password.txt', 'r') as file:
                password = file.read().strip()
        from .apis.account_api import bcrypt
        db.session.add(User('admin', 'none-required', bcrypt.generate_password_hash(password)))
        db.session.commit()
        print('added super user!')
    else:
        print('super user already exists')


def create_app(config_name='default'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    # enable CORS
    # CORS(app, resources={r'/*': {'origins': '*'}})
    CORS(app, supports_credentials=True)

    # Add routes
    from .apis.image_api import image_api
    app.register_blueprint(image_api)
    with app.app_context():
        from .apis.account_api import account_api
        app.register_blueprint(account_api)

    # Create & setup LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Add CLI custom commands
    from .cli import create_all, drop_all
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Add CLI custom commands
    from .cli import create_all, drop_all
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    # init database
    with app.app_context():
        db.create_all()
        create_super_user()
        discover_all_banks()

    app.config['SECRET_KEY'] = '766574a7486ff3209b5b2a347a854f168d0a5d2af588b681cf592fb7f61f99e2'

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
