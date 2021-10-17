"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request, make_response, Response
from ..database.access import db
from flask_cors import cross_origin
from ..database.models import ImageToAnnotate

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

    # method = request.method

    # image_bank = request.json.get('image_bank') or 'null image_bank'
    # image_file = request.json.get("image_file") or 'null image_file'
    # res = make_response(jsonify(image_bank = image_bank, image_file = image_file, method = method))
    # res.status = 200

    # return res
    pic = request.files["pic"]

    if not pic:
        return 'No pic uploaded', 400

    image_bank_id = 1
    # image_bank = "butterfly"
    file_url = "file_url"
    # There may be some issues with database
    img = pic.read()

    imageToAnnotate = ImageToAnnotate(image_bank_id=image_bank_id, file_url=file_url, img=img)
    db.session.add(imageToAnnotate)
    db.session.commit()

    return 'Image has been uploaded', 200

@image_api.route('/api/image/get/<int:id>')
def get_img(id):
    img = ImageToAnnotate.query.filter_by(id=id).first()
    if not img:
        return 'No image with that id', 404

    return Response(img.img)
