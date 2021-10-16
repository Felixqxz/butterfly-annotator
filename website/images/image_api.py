"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request
from ..database.access import db

image_api = Blueprint('image_api', __name__)

@image_api.route('/api/bank/<bank>', methods=['GET'])
def list_images(bank):
    images = []
    for i in range(3):
        images.append({
            'id': i,
            'url': 'https://cdn.mos.cms.futurecdn.net/MutKXr3Z2za46Zdi3XM3BM-1200-80.jpg',
            'fullDescription': 'A very pretty butterfly!',
        })
    bankName = "dummy"
    return jsonify({
        'bankName': bankName,
        'images': images,
    }) # TODO

@image_api.route('/api/images', methods=['GET'])
def get_all_images():
    images = []
    images.append({
        'id': 1,
        'url': 'https://cdn.mos.cms.futurecdn.net/MutKXr3Z2za46Zdi3XM3BM-1200-80.jpg'
    })
    return jsonify({
        'bankName': 'Butterfly',
        'images': images
    })

@image_api.route('/api/test', methods=['GET'])
def get_all_images_from_database():
    images = []
    images.append({
        'id': 1,
        'url': 'https://cdn.mos.cms.futurecdn.net/MutKXr3Z2za46Zdi3XM3BM-1200-80.jpg'
    })
    return jsonify({
        'bankName': 'Butterfly',
        'images': images
    })

@image_api.route('/api/image/upload', methods=['POST'])
def upload_image(image):
    image_bank = request.form.get("image_bank")
    image_file = request.form.get("image_file")
    return image_bank + image_file
