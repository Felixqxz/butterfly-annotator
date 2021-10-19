from flask import Flask, request, flash, session
from flask_cors import CORS
from flask_login import LoginManager
from .database.access import db
from .config import config_by_name
from .database.loaders import setup_user_loader
from flask_login import login_user, current_user, logout_user
from .database.models import User
from flask_bcrypt import Bcrypt
from flask.json import jsonify

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
    from .images.image_api import image_api
    app.register_blueprint(image_api)
    # Create & setup LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = "info"
    setup_user_loader(login_manager)

    
    # Add CLI custom commands
    from .cli import create_all, drop_all
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    # done
    return app

app = create_app()

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '766574a7486ff3209b5b2a347a854f168d0a5d2af588b681cf592fb7f61f99e2'

@app.route('/register', methods=['POST'])
def register():
    user_info = request.get_json(force=True)
    username = user_info.get("username")
    email = user_info.get('email')
    password = user_info.get('password') 

    user = db.session.query(User).filter(User.username == username).first()
    if user:
        return jsonify({"status": 401,    
                       "data": {"message": "User already exists"}})
    else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Logged in successfully.')
        return jsonify({"status": 200, "data": {"username": user.username, "email": user.email}})


@app.route('/login', methods=['POST'])
def login():
    if current_user.get_id() != None:
        return jsonify({"status": 401,    
                       "data": {"message": "User already logged in"}})

    user_info = request.get_json(force=True)
    username = user_info.get('username')
    password = user_info.get('password') 
    
    user = db.session.query(User).filter(User.username == username).first()
    if user:
        if bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.')
            return jsonify({"status": 200, "data": {"username": user.username, "email": user.email}})
        else:
            return jsonify({"status": 401,    
                       "data": {"message": "Password incorrect"}})
    else:
        return jsonify({"status": 401,    
                       "data": {"message": "Username or password error"}})

@app.route('/logout', methods=['POST'])
def logout():
    if current_user.get_id() != None:
        logout_user()
        return jsonify({"status": 200,
                        "data": {"message": "Log out success"}})
    else:
        return jsonify({"status": 401,    
                       "data": {"message": "Log out fail"}})

if __name__ == '__main__':
    app.run()
