import os

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from .config import config_by_name
from .db import db


def create_app(config_name=None):
    # create and configure the app
    app = Flask(__name__)

    if config_name is None:
        app.config.from_object(config_by_name["default"])
    else:
        app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # sanity check route
    @app.route('/', methods=['GET'])
    def ping_pong():
        return jsonify('Hello World!')

    return app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username