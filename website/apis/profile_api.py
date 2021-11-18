"""
The part of the API is used for profile page
"""
from flask.json import jsonify
from flask import Blueprint, request
from flask_login import login_required, current_user, login_user, logout_user
from http import HTTPStatus
import os
from ..database.access import db
from ..database.models import User

profile_api = Blueprint('profile_api', __name__)
basedir = os.path.abspath(os.path.dirname(__name__))

@profile_api.route('/api/avatar/upload', methods=['POST'])
def upload_avatar():

    avatarName = request.form.get('avatarName')
    avatar_image = request.files['avatarFile']
    username = request.form.get('username')
    description = request.form.get('description')
    if (avatarName != "null"):
        path = basedir + "/website/static/avatar/"
        avatar_path = path + avatarName
        avatar_image.save(avatar_path)

        # In this case, the avater changed
        db.session.query(User).filter(User.username == username)\
            .update({ 
                User.avatar_name: avatarName,
                User.description: description
            })
        db.session.commit()
        return "200" # need to change
    else:
        # Only description changed in this case
        db.session.query(User).filter(User.username == username)\
            .update({ 
                User.description: description
            })
        db.session.commit()
        return "200" # need to change


@profile_api.route('/api/avatar/get', methods=['GET'])
def get_avatar():
    print(current_user.avatar_name)
    return jsonify({
        'avatar': current_user.avatar_name,
        'description': current_user.description
        })


@profile_api.route('/api/info/get', methods=['GET'])
def get_info():
    return jsonify({
        'firstName': current_user.first_name,
        'lastName': current_user.last_name,
        'email': current_user.email,
        })


@profile_api.route('/api/info/update', methods=['POST'])
@login_required
def update_info():

    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')

    db.session.query(User).filter(User.username == current_user.username)\
      .update({ 
        User.first_name: firstName,
        User.last_name: lastName,
        User.email: email
    })
    db.session.commit()
    return "200"
    # if (username == ""):
    #   db.session.query(User).filter(User.username == current_user.username)\
    #     .update({ 
    #       User.first_name: firstName,
    #       User.last_name: lastName,
    #       User.email: email,
    #   })
    #   db.session.commit()
    #   return "200"
    # else:
    #   user = db.session.query(User).filter(User.username == username).first()
    #   if user:
    #     return jsonify({"message": "User already exists"}), HTTPStatus.UNAUTHORIZED
    #   else:
    #     db.session.query(User).filter(User.username == current_user.username)\
    #       .update({ 
    #         User.first_name: firstName,
    #         User.last_name: lastName,
    #         User.email: email,
    #         User.username: username
    #     })
    #     # print(user)
    #     db.session.commit()
    #     user = db.session.query(User).filter(User.username == username).first()
    #     print(user)
    #     logout_user()
    #     login_user(user)
    #     return "200" # need to change
    