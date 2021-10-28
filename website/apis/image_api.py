"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request
from flask_login import login_required, current_user
from http import HTTPStatus
import os
from ..database.access import db
from ..database.models import ImageToAnnotate, ImageAnnotation
from ..images.geometry import PolygonalRegion

basedir = os.path.abspath(os.path.dirname(__name__))
image_api = Blueprint('image_api', __name__)

bank_access_levels = {
    'admin': 90,
    'editor': 50,
    'viewer': 0,
}


def can_access_image(image, user, access_level='viewer'):
    """
    Returns `True` iff the given user can access the provided image.
    """
    level = bank_access_levels[access_level]
    return image.image_bank.id in [access.bank_id for access in user.accesses 
        if access.permission_level >= level]


def ensure_image_exists(raw_id):
    """
    Ensures the provided id is a valid image id and that an image with
    that id exists in the database.
    """
    if not raw_id.isnumeric():
        return None
    image_id = int(raw_id)
    return db.session.query(ImageToAnnotate).filter(ImageToAnnotate.id == image_id).first()


@image_api.route('/api/bank-list', methods=['GET'])
@login_required
def list_banks():
    """
    Returns the list of banks available to the current user.
    """
    banks = []
    for access in current_user.accesses:
        banks.append({
            'id': access.bank.id,
            'name': access.bank.bankname,
            'description': access.bank.description
        })
    return jsonify(banks)


# This route allows to fetch the list of images of a given bank.
@image_api.route('/api/bank/<bank_id>', methods=['GET'])
@login_required
def list_images(bank_id):
    if not bank_id.isnumeric():
        return jsonify({'error': 'ill-formed request'}), HTTPStatus.BAD_REQUEST
    banks_dict = {access.bank_id: access.bank for access in current_user.accesses}
    bank_id = int(bank_id)
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

    path = basedir + '/website/static/source_images/'
    file_path = path + pic.filename
    pic.save(file_path)

    image_bank_id = 1
    # TODO convert to path relative to the folder containing the banks
    file_url = '../../../website/static/source_images/' + pic.filename

    image_to_annotate = ImageToAnnotate(image_bank_id=image_bank_id, file_url=file_url)
    db.session.add(image_to_annotate)
    db.session.commit()

    return jsonify({
        'image_bank_id': image_bank_id,
        'image_name': pic.filename,
        'method': method
    })


# This route is used to get all images info that user uploaded.
@image_api.route('/api/image/getImage', methods=['GET'])
@login_required
def get_image():  # TODO: remove this endpoint
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
        'bankName': 'Butterfly',
        'images': images
    })


@image_api.route('/api/image/annotate', methods=['PUT'])
@login_required
def insert_annotation():
    """
    Allows to push all the annotations of the image to the database.
    """
    req = request.get_json()
    image = ensure_image_exists(req['image_id'])
    if image is None:
        return jsonify({'error': 'there exists no image with such an id'}), HTTPStatus.NOT_FOUND
    if 'annotations' not in req:
        return jsonify({'result': 'success'})
    if not can_access_image(image, current_user, access_level='editor'):
        return jsonify({'error': 'not authorized to annotate this bank'}), HTTPStatus.UNAUTHORIZED
    # first pass: verify all data
    for annotation in req['annotations']:
        try:
            region = PolygonalRegion(annotation['points'])
        except Exception:
            return jsonify({'error': 'ill-formed polygonal region'}), HTTPStatus.BAD_REQUEST
        if max(map(lambda p: p.x, region.points)) > image.width or \
                min(map(lambda p: p.x, region.points)) < 0 or \
                max(map(lambda p: p.y, region.points)) > image.height or \
                min(map(lambda p: p.y, region.points)) < 0:
            return jsonify({'error': 'there exists a point out of bounds'}), HTTPStatus.BAD_REQUEST
        if annotation['id'] != '-1':
            # trying to update existing annotation
            if int(annotation['id']) not in [annot.id for annot in image.annotations]:
                return jsonify({'error': 'trying to update an annotation that does not exist'}), HTTPStatus.BAD_REQUEST

    # second pass: update database
    for annotation in req['annotations']:
        region = PolygonalRegion(annotation['points'])
        stripped_tag = annotation['tag'].strip().tolower()
        if annotation['id'] == '-1':
            # new region
            a = ImageAnnotation(image.id, stripped_tag, region.sql_serialize_region())
            db.session.add(a)
            db.session.commit()
        else:
            db.session.query(ImageAnnotation)\
                .filter(ImageAnnotation.id == int(annotation['id']))\
                .update({
                    ImageAnnotation.region_info: region.sql_serialize_region(),
                    ImageAnnotation.tag: stripped_tag
                })
            db.session.commit()
    return jsonify({'result': 'success'})


@image_api.route('/api/image/annotations/<image_id>')
@login_required
def get_annotations(raw_id):
    """
    Returns the annotations of the image with id `image_id`.
    """
    image = ensure_image_exists(raw_id)
    if image is None:
        return jsonify({'message': 'there is no image with such an id'}), HTTPStatus.NOT_FOUND
    if not can_access_image(image, current_user):
        return jsonify({'message': 'not authorized to view this bank'})
    return jsonify({
        'id': image.id,
        'annotations': [
            {
                'id': annotation.id,
                'tag': annotation.tag,
                'regionInfo': annotation.region_info,
            } for annotation in image.annotations
        ]
    })
