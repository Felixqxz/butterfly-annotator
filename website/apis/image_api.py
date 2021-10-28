"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request, escape
from flask_login import login_required, current_user
from http import HTTPStatus
import os
from ..database.access import db
from ..database.models import User, BankAccess, ImageToAnnotate, ImageAnnotation, ImageBank
from ..images.geometry import PolygonalRegion

basedir = os.path.abspath(os.path.dirname(__name__))
image_api = Blueprint('image_api', __name__)


bank_access_levels = {
    'super-admin': 100,  # reserved: one such account per app instance
    'admin': 90,
    'moderator': 70,  # allows to annotate and manage other editors/viewers
    'editor': 50,  # only allows to annotate
    'viewer': 0,
}


def can_access_bank(bank, user, access_level='viewer'):
    """
    Returns `True` iff the given user can access the provided bank.
    """
    level = bank_access_levels[access_level]
    return bank.id in [access.bank_id for access in user.accesses 
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


def get_bank_access_level(user, bank_id):
    """
    Returns the BankAccess object for the given user and the given
    bank.
    """
    bank_access = [access for access in user.accesses 
        if access.bank_id == bank_id]
    return bank_access[0] if bank_access else None 


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


@image_api.route('/api/bank-create', methods=['POST'])
@login_required
def create_image_bank():
    data = request.get_json()
    if 'bankName' not in data or 'description' not in data:
        return jsonify({'error': 'a bank needs a description and a name'}), HTTPStatus.BAD_REQUEST
    bankname = escape(data['bankName'])
    if db.session.query(ImageBank).filter(ImageBank.bankname == bankname).first() is not None:
        return jsonify({'error': 'a bank with the same name already exists'}), HTTPStatus.UNAUTHORIZED
    newBank = ImageBank(bankname, escape(data['description']))
    db.session.add(newBank)
    db.session.commit()
    # allow creator to see his new bank
    db.session.add(BankAccess(current_user.get_id(), newBank.id, bank_access_levels['admin']))
    db.session.commit()
    return jsonify({
        'id': newBank.id,
        'bankName': newBank.bankname,
        'description': newBank.description
    })


@image_api.route('/api/bank-access', methods=['PUT'])
@login_required
def manage_access_bank():
    data = request.get_json()
    if 'id' not in data or 'targetName' not in data or 'level' not in data:
        return jsonify({'error': 'missing field'}), HTTPStatus.BAD_REQUEST
    if not data['id'].isnumeric():
        return jsonify({'error': 'invalid bank id'}), HTTPStatus.BAD_REQUEST
    level_raw = data['level']
    if not level_raw.isnumeric() or int(level_raw) < -1 or int(level_raw) > 90:
        # the maximal assignable level is admin (super-admin is reserved)
        return jsonify({'error': 'invalid permission level'})
    level = int(data['level'])
    # search target user
    target_user = db.session.query(User).filter(User.username == escape(data['targetName']))
    if target_user is None:
        return jsonify({'error': 'no such target user'}), HTTPStatus.NOT_FOUND
    bank = db.session.query(ImageBank).filter(ImageBank.id == int(data['id'])).first()
    if bank is None:
        return jsonify({'error': 'no such bank'}), HTTPStatus.NOT_FOUND
    user_access = get_bank_access_level(current_user, bank.id)
    if not user_access:
        return jsonify({'error': 'you do not have access to this bank'}), HTTPStatus.UNAUTHORIZED
    # now that bank & target exist and are accessible,
    # check for permission levels
    if user_access.permission_level < bank_access_levels['moderator']:
        return jsonify({'error': 'insufficient permissions'}), HTTPStatus.UNAUTHORIZED
    if level >= bank_access_levels['moderator'] and user_access.permission_level < user_access['admin']:
        # only admins can assign other admins and moderators
        return jsonify({'error': 'insufficient permissions'}), HTTPStatus.UNAUTHORIZED
    target_access = get_bank_access_level(target_user, bank.id)
    if not target_access or target_access.permission_level < user_access.permission_level:
        # the originating user is able to edit access for target
        target_query = db.session.query(BankAccess).filter(BankAccess.user_id == target_user.id)
        if level == -1:
            if target_access:
                target_query.delete()
                db.session.commit()
            # else: user is trying to remove a user that has already no access (ignore)
        else:
            if target_access:
                target_query.update({ BankAccess.permission_level: level })
                db.session.commit()
            else:
                db.session.add(BankAccess(target_user.id, bank.id, level))
                db.session.commit()
        return jsonify({'message': 'success'})
    # user is trying to update permissions of someone of the same rank
    return jsonify({'error': 'insufficient permissions'}), HTTPStatus.UNAUTHORIZED


@image_api.route('/api/bank/<bank_id>', methods=['GET'])
@login_required
def list_images(bank_id):
    """
    Returns the list of the images of a given endpoint.
    """
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
    # TODO: fix this here; might remove this whole endpoint
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


@image_api.route('/api/image/annotate', methods=['POST'])
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
    if not can_access_bank(image.image_bank, current_user, access_level='editor'):
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
            a = ImageAnnotation(image.id, stripped_tag, region.sql_serialize_region(), current_user.get_id())
            db.session.add(a)
            db.session.commit()
        else:
            db.session.query(ImageAnnotation)\
                .filter(ImageAnnotation.id == int(annotation['id']))\
                .update({
                    ImageAnnotation.region_info: region.sql_serialize_region(),
                    ImageAnnotation.tag: stripped_tag,
                    ImageAnnotation.author_id: current_user.get_id()
                })
            db.session.commit()
    return jsonify({'result': 'success'})


@image_api.route('/api/image/annotations/<image_id>', methods=['GET'])
@login_required
def get_annotations(raw_id):
    """
    Returns the annotations of the image with id `image_id`.
    """
    image = ensure_image_exists(raw_id)
    if image is None:
        return jsonify({'message': 'there is no image with such an id'}), HTTPStatus.NOT_FOUND
    if not can_access_bank(image.image_bank, current_user):
        return jsonify({'message': 'not authorized to view this bank'}), HTTPStatus.UNAUTHORIZED
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
