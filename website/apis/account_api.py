from flask import Blueprint, current_app, request, jsonify
from flask_login import current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from ..database.models import User
from ..database.access import db

account_api = Blueprint('account_api', __name__)
bcrypt = Bcrypt(current_app)


@account_api.route('/register', methods=['POST'])
def register():
    user_info = request.get_json(force=True)
    username = user_info.get('username')
    email = user_info.get('email')
    password = user_info.get('password')

    user = db.session.query(User).filter(User.username == username).first()
    test_duplicate_email = db.session.query(User).filter(User.email == email).first()

    if user:
        return jsonify({'status': 401,
                        'message': 'User already exists'})
    if test_duplicate_email:
        return jsonify({'status': 401,
                        'message': 'Email already exists'})
    else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        return jsonify({'status': 200, 'data': {'username': user.username, 'email': user.email},
                        'message': 'Registered successfully!'})


@account_api.route('/login', methods=['POST'])
def login():
    if current_user.get_id() is not None:
        return jsonify({'status': 401,
                        'message': 'User already logged in'})

    user_info = request.get_json(force=True)
    username = user_info.get('username')
    password = user_info.get('password')

    user = db.session.query(User).filter(User.username == username).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            # TODO: do not use raw answers: make_response
            return jsonify({'status': 200, 'data': {'username': user.username, 'email': user.email},
                            'message': 'Login successful!'})
        else:
            return jsonify({'status': 401,
                            'message': 'Password incorrect'})
    else:
        return jsonify({'status': 401,
                        'message': 'Username does not exist'})


@account_api.route('/logout', methods=['POST'])
def logout():
    if current_user.get_id() is not None:
        logout_user()
        return jsonify({'status': 200,
                        'message': 'Log out success'})
    else:
        return jsonify({'status': 401,
                        'message': 'Not logged in'})
