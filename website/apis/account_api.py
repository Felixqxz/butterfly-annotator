import os

from flask import Blueprint, current_app, request, jsonify, send_file
from flask_login import current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from http import HTTPStatus
from ..database.models import User
from ..database.access import db

account_api = Blueprint('account_api', __name__)
bcrypt = Bcrypt(current_app)
avatars_dir = os.getcwd() + os.sep + 'avatars'
if not os.path.exists(avatars_dir):
    os.mkdir(avatars_dir)


@account_api.route('/register', methods=['POST'])
def register():
    user_info = request.get_json()
    username = user_info.get('username')
    email = user_info.get('email')
    password = user_info.get('password')

    user = db.session.query(User).filter(User.username == username).first()
    duplicate_email = db.session.query(User).filter(User.email == email).first()

    if user:
        return jsonify({'message': 'User already exists'}), HTTPStatus.UNAUTHORIZED
    if duplicate_email:
        return jsonify({'message': 'Email already exists'}), HTTPStatus.UNAUTHORIZED
    else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify({'username': user.username, 'email': user.email})


@account_api.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'User already logged in'}), HTTPStatus.UNAUTHORIZED

    user_info = request.get_json(force=True)
    username = user_info.get('username')
    password = user_info.get('password')

    user = db.session.query(User).filter(User.username == username).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({'username': user.username, 'email': user.email})
        else:
            return jsonify({'message': 'Incorrect password'}), HTTPStatus.UNAUTHORIZED
    else:
        return jsonify({'message': 'User does not exist'}), HTTPStatus.NOT_FOUND


@account_api.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Log out success'})
    else:
        return jsonify({'message': 'Not logged in'}), HTTPStatus.UNAUTHORIZED


@account_api.route('/api/profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if not request.files:
        return jsonify({'message': 'no file provided'})
    picture = request.files['file']
    location = os.path.join(avatars_dir, current_user.username + '.jpg')
    if os.path.isfile(location):
        os.remove(location)
    picture.save(location)
    current_user.has_profile_picture = True
    db.session.commit()
    return jsonify({'message': 'OK'})


@account_api.route('/api/profile-picture/<username>', methods=['GET'])
@login_required
def get_profile_picture(username):
    if not username:
        return jsonify({'message': 'no username provided'}), HTTPStatus.BAD_REQUEST
    user = db.session.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({'message': 'no such user'}), HTTPStatus.NOT_FOUND
    if user.has_profile_picture:
        location = os.path.join(avatars_dir, user.username + '.jpg')
        return send_file(location, mimetype='image/jpeg')
    # not an error, just no picture!
    return jsonify({'message': 'no profile picture'})


@account_api.route('/api/user-info/<username>', methods=['GET'])
@login_required
def get_user_info(username):
    if not username:
        return jsonify({'message': 'no username provided'}), HTTPStatus.BAD_REQUEST
    user = db.session.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({'message': 'no such user'}), HTTPStatus.NOT_FOUND
    return jsonify({
        'username': user.username,
        'email': user.email,
    })
