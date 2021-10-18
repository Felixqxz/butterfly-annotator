"""
The part of the API that allows users to sign in and register.
"""
from flask.json import jsonify
from flask import Flask, request, flash
from flask_login import login_user, current_user
from database.access import db
from database.models import User
from website import app

app.login_manager.login_view = 'login'


@app.route('/login', methods=['POST'])
def login():
    if current_user.get_id() != None:
        return jsonify({"status": 401,    
                        "reason": "User already logged in"})

    user_info = request.get_json()
    username = user_info.get('username')
    password = user_info.get('password') 
    # user = User.objects(name=username,
    #                     password_hash=password).first()
    user = db.session.query(User).filter(User.username == username)
    if user:
        login_user(user)
        flash('Logged in successfully.')
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

    user = db.session.query(User).filter(User.username == username).first()
    if user:
        return jsonify({"status": 401,
                        "reason": "Username already exists"})
    else:
        user = User(name=username, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Logged in successfully.')
        return jsonify(user.to_json())