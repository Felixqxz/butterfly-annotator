"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint

image_api = Blueprint('image_api', __name__)

@image_api.route('/api/dir/<bank>', methods=['GET'])
def list_images(bank):
    return jsonify({'bank': bank}) # TODO
