"""
The part of the API that allows users to sign in and register.
"""
from flask.json import jsonify
from flask import Flask, request
from flask_login import LoginManager, login_manager, login_user
from database.access import db
from database.models import User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
login_manager = LoginManager()

login_manager.login_view = 'login'


@app.route('/login', methods=['POST'])
def login():
    user_info = request.get_json()
    username = user_info.get('username')
    password = user_info.get('password') 
    user = User.objects(name=username,
                        password_hash=password).first()
    if user:
        login_user(user)
        # TODO
        return jsonify(user.to_json())
    else:
        return jsonify({"status": 401,    
                        "reason": "Username or Password Error"})


@app.route('/register', methods=['POST'])
def register():
    user_info = request.get_json()
    username = user_info.get('username')
    email = user_info.get('email')
    password = user_info.get('password') 

    user = User.objects(name=username).first()
    if user:
        return jsonify({"status": 401,
                        "reason": "Username already exists"})
    else:
        user = User(name=username, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        # TODO
        return jsonify(user.to_json())