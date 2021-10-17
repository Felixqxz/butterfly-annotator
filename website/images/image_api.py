"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request, make_response
from ..database.access import db
from flask_cors import cross_origin

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

@image_api.route('/api/image/upload', methods=['POST'])
def upload_image():

    method = request.method

    image_bank = request.json.get('image_bank') or 'null image_bank'
    image_file = request.json.get("image_file") or 'null image_file'
    res = make_response(jsonify(image_bank = image_bank, image_file = image_file, method = method))
    res.status = 200

    return res
    
