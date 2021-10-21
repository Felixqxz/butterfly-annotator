"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint

image_api = Blueprint('image_api', __name__)


@image_api.route('/api/bank-list', methods=['GET'])
def list_banks():
    banks = []
    for i in range(7):
        banks.append({
            'id': i,
            'name': 'Coucou ' + str(i),
            'description': 'This is the bank number ' + str(i),
        })
    return jsonify(banks)


@image_api.route('/api/bank/<bank>', methods=['GET'])
def list_images(bank):
    images = []
    for i in range(7):
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
