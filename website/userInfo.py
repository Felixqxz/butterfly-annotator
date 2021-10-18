from flask_login import login_user, current_user
from .database.models import User
from flask_bcrypt import Bcrypt
from flask.json import jsonify
from flask import Flask, request, flash, session
from .database.access import db
from website import app, bcypt

# bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    user_info = request.get_json(force=True)
    username = user_info.get("username")
    email = user_info.get('email')
    password = user_info.get('password') 

    user = db.session.query(User).filter(User.username == username).first()
    if user:
        return jsonify({"status": 401,
                        "reason": "Username already exists"})
    else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Logged in successfully.')
        return jsonify({"status": 200})


@app.route('/login', methods=['POST'])
def login():
    if current_user.get_id() != None:
        return jsonify({"status": 401,    
                        "reason": "User already logged in"})

    user_info = request.get_json(force=True)
    username = user_info.get('username')
    password = user_info.get('password') 
    
    user = db.session.query(User).filter(User.username == username).first()
    if user:
        if bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.')
            return jsonify({"status": 200})
        else:
            return jsonify({"status": 401,    
                        "reason": "Password incorrect"})
    else:
        return jsonify({"status": 401,    
                        "reason": "Username or Password Error"})