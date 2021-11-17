from flask import Blueprint, current_app, request, jsonify
from flask_login import current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from http import HTTPStatus
from ..database.models import User
from ..database.access import db
import os

account_api = Blueprint('account_api', __name__)
bcrypt = Bcrypt(current_app)
basedir = os.path.abspath(os.path.dirname(__name__))


@account_api.route('/register', methods=['POST'])
def register():
    user_info = request.get_json()
    username = user_info.get('username')
    email = user_info.get('email')
    password = user_info.get('password')

    user = db.session.query(User).filter(User.username == username).first()
    if user:
        return jsonify({"message": "User already exists"}), HTTPStatus.UNAUTHORIZED
    else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=password_hash)
        avatar_name = ""
        user.avatar_name = avatar_name
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify({"username": user.username, "email": user.email})


@account_api.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "user already logged in"}), HTTPStatus.UNAUTHORIZED

    user_info = request.get_json(force=True)
    username = user_info.get('username')
    password = user_info.get('password')

    user = db.session.query(User).filter(User.username == username).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({"username": user.username, "email": user.email, "avatar": user.avatar_name})
        else:
            return jsonify({"message": "incorrect password"}), HTTPStatus.UNAUTHORIZED
    else:
        return jsonify({"message": "no user with such username"}), HTTPStatus.NOT_FOUND


@account_api.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Log out success"})
    else:
        return jsonify({"message": "Not logged in"}), HTTPStatus.UNAUTHORIZED
