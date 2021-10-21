"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request, make_response, Response
import os
from ..database.access import db
from flask_cors import cross_origin
from ..database.models import ImageToAnnotate

basedir = os.path.abspath(os.path.dirname(__name__))
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

# This api is used to upload an image
@image_api.route('/api/image/upload', methods=['POST'])
def upload_image():

    method = request.method
    pic = request.files['imgFile']

    if not pic:
        return 'No pic uploaded', 400

    path = basedir + "/website/static/source_images/"
    file_path = path + pic.filename
    pic.save(file_path)

    image_bank_id = 1
    # image_bank = "Butterfly"
    file_url = "../../../website/static/source_images/" + pic.filename

    imageToAnnotate = ImageToAnnotate(image_bank_id=image_bank_id, file_url=file_url, image_name=pic.filename)
    db.session.add(imageToAnnotate)
    db.session.commit()

    return jsonify({
        'status': 200,
        'image_bank_id': image_bank_id,
        'image_name': pic.filename,
        'method': method
    })

# This api is used to get all images info that user uploaded
@image_api.route('/api/image/getImage', methods=['GET'])
def get_image():
    images = []
    count = ImageToAnnotate.query.filter_by(image_bank_id=1).count()
    for i in range(count):
        image = ImageToAnnotate.query.filter_by(id=i+1).first()
        images.append({
            'id': i,
            'url': image.file_url,
            'imageName': image.image_name,
        })
    
    return jsonify({
        'status': 200,
        'bankName': 'Butterfly',
        'images': images
    })
