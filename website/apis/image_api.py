"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request
from flask_login import login_required, current_user
from http import HTTPStatus
import os
from ..database.access import db
from ..database.models import ImageToAnnotate

basedir = os.path.abspath(os.path.dirname(__name__))
image_api = Blueprint('image_api', __name__)


# This route allows to fetch the list of banks a user can see.
@image_api.route('/api/bank-list', methods=['GET'])
@login_required
def list_banks():
    banks = []
    for access in current_user.accesses:
        banks.append({
            'id': access.bank.id,
            'name': access.bank.bankname,
            'description': access.bank.description
        })
    return jsonify(banks)


# This route allows to fetch the list of images of a given bank.
@image_api.route('/api/bank/<bank>', methods=['GET'])
@login_required
def list_images(bank):
    if not bank.isnumeric():
        return jsonify({'error': 'ill-formed request'}), HTTPStatus.BAD_REQUEST
    banks_dict = {b.bank_id: b for b in current_user.accesses}
    bank_id = int(bank)
    if bank_id not in banks_dict:
        return jsonify({'error': 'you do not have access to this bank'}), HTTPStatus.UNAUTHORIZED
    return {
        'bankName': banks_dict[bank_id].bankname,
        'images': [
            {
                'id': image.id,
                'url': image.file_url,
                'fullDescription': image.description,
            } for image in banks_dict[bank_id].images
        ]}


# This route is used to upload an image.
@image_api.route('/api/image/upload', methods=['POST'])
@login_required
def upload_image():
    # TODO: fix this here
    method = request.method
    pic = request.files['imgFile']

    if not pic:
        return 'No pic uploaded', HTTPStatus.BAD_REQUEST

    path = basedir + "/website/static/source_images/"
    file_path = path + pic.filename
    pic.save(file_path)

    image_bank_id = 1
    # image_bank = "Butterfly"
    file_url = "../../../website/static/source_images/" + pic.filename

    image_to_annotate = ImageToAnnotate(image_bank_id=image_bank_id, file_url=file_url, image_name=pic.filename)
    db.session.add(image_to_annotate)
    db.session.commit()

    return jsonify({
        'status': 200,  # TODO: remove this
        'image_bank_id': image_bank_id,
        'image_name': pic.filename,
        'method': method
    })


# This route is used to get all images info that user uploaded.
@image_api.route('/api/image/getImage', methods=['GET'])
@login_required
def get_image():
    images = []
    count = ImageToAnnotate.query.filter_by(image_bank_id=1).count()
    for i in range(count):
        image = ImageToAnnotate.query.filter_by(id=i + 1).first()  # TODO: what is this?
        images.append({
            'id': i,
            'url': image.file_url,
            'imageName': '',  # Removed image's name!
        })

    return jsonify({
        'status': 200,  # TODO: remove this
        'bankName': 'Butterfly',
        'images': images
    })
