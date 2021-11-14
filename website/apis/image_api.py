"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request, escape, send_file
from flask_login import login_required, current_user
from sqlalchemy import and_, desc
from http import HTTPStatus
import os
from ..database.access import db
from ..database.models import User, BankAccess, ImageToAnnotate, ImageAnnotation, ImageBank
from ..images.geometry import PolygonalRegion
from ..images.discovery import default_bank_directory

basedir = os.path.abspath(os.path.dirname(__name__))
image_api = Blueprint('image_api', __name__)

TERM_LIST_PATH = 'termlist'
ADJ_LIST_PATH = 'adjlist.txt'
COLOR_LIST_PATH = 'colorlist.txt'
PATTERN_LIST_PATH = 'patternlist.txt'
PATTERN_VERBS_PATH = 'patternverbs.txt'

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

def get_keywords(description):
    # fourth line of the file is always the description.
    words = (description.split('\n')[3]).split()
    adj_list = []
    pattern_list = []
    keywords = []

    adj_list_path = os.path.join(TERM_LIST_PATH, ADJ_LIST_PATH)
    color_list_path = os.path.join(TERM_LIST_PATH, COLOR_LIST_PATH)
    pattern_list_path = os.path.join(TERM_LIST_PATH, PATTERN_LIST_PATH)
    pattern_verbs_path = os.path.join(TERM_LIST_PATH, PATTERN_VERBS_PATH)

    if os.path.isfile(adj_list_path):
        with open(adj_list_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                adj_list.append(line.rstrip())

    if os.path.isfile(color_list_path):
        with open(color_list_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                adj_list.append(line.rstrip())

    if os.path.isfile(pattern_verbs_path):
        with open(pattern_verbs_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                adj_list.append(line.rstrip())

    if os.path.isfile(pattern_list_path):
        with open(pattern_list_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                pattern_list.append(line.rstrip()) 
    
    start_index = -1
    end_index = -1
    for word in words:
        for adj_word in adj_list:
            if word == adj_word:
                start_index = description.find(word, start_index+len(word))
                print(start_index)
        for pattern_word in pattern_list:
            if word == pattern_word:
                end_index = description.find(word, end_index+len(word)) + len(word)
                if end_index > start_index and start_index not in [pair[0] for pair in keywords]:
                    pair = [start_index, end_index]
                    keywords.append(pair)
    return keywords


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


@image_api.route('/api/bank-access', methods=['PUT'])
@login_required
def manage_access_bank():
    data = request.get_json()
    if 'id' not in data or 'targetName' not in data or 'level' not in data:
        return jsonify({'error': 'missing field'}), HTTPStatus.BAD_REQUEST
    if not data['id'].isnumeric():
        return jsonify({'error': 'invalid bank id'}), HTTPStatus.BAD_REQUEST
    level = data['level']
    if level < -1 or level > 90:
        # the maximal assignable level is admin (super-admin is reserved)
        return jsonify({'error': 'invalid permission level'}), HTTPStatus.UNAUTHORIZED
    # search target user
    target_user = db.session.query(User).filter(User.username == escape(data['targetName'])).first()
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


@image_api.route('/api/bank-list-accesses/<bank_id>', methods=['GET'])
@login_required
def list_bank_accesses(bank_id):
    if not bank_id.isnumeric():
        return jsonify({'error': 'invalid bank id'}), HTTPStatus.BAD_REQUEST
    bank = db.session.query(ImageBank).filter(ImageBank.id == int(bank_id)).first()
    if bank is None:
        return jsonify({'error': 'no such bank'}), HTTPStatus.NOT_FOUND
    if not can_access_bank(bank, current_user):
        return jsonify({'error': 'you do not have access to this bank'}), HTTPStatus.UNAUTHORIZED
    return jsonify({
        'users': [
            {
                'username': access.user.username,
                'level': access.permission_level,
            } for access in db.session.query(BankAccess).filter(BankAccess.bank_id == bank.id).all()
        ]
    })


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
                'url': 'image-serve/' + image.file_url,
                'fullDescription': image.description,
            } for image in banks_dict[bank_id].images
        ]}


@image_api.route('/api/image/annotate', methods=['POST'])
@login_required
def insert_annotation():
    """
    Allows to push all the annotations of the image to the database.
    """
    req = request.get_json()
    image = ensure_image_exists(req['imageId'])
    if image is None:
        return jsonify({'error': 'there exists no image with such an id'}), HTTPStatus.NOT_FOUND
    if 'annotations' not in req:
        return jsonify({'result': 'success'})
    if not can_access_bank(image.image_bank, current_user, access_level='editor'):
        return jsonify({'error': 'not authorized to annotate this bank'}), HTTPStatus.UNAUTHORIZED
    # first pass: verify all data
    for annotation in req['annotations']:
        try:
            region = PolygonalRegion.deserialize_from_json(annotation['points'])
        except Exception:
            return jsonify({'error': 'ill-formed polygonal region'}), HTTPStatus.BAD_REQUEST
        if max(map(lambda p: p.x, region.points)) > image.width or \
                min(map(lambda p: p.x, region.points)) < 0 or \
                max(map(lambda p: p.y, region.points)) > image.height or \
                min(map(lambda p: p.y, region.points)) < 0:
            print("mais oui c'est clair !!!")
            return jsonify({'error': 'there exists a point out of bounds'}), HTTPStatus.BAD_REQUEST
        if annotation['id'] != -1:
            # trying to update existing annotation
            if int(annotation['id']) not in [annot.id for annot in image.annotations]:
                return jsonify({'error': 'trying to update an annotation that does not exist'}), HTTPStatus.BAD_REQUEST

    # second pass: update database
    for annotation in req['annotations']:
        region = PolygonalRegion.deserialize_from_json(annotation['points'])
        stripped_tag = annotation['tag'].strip().lower()
        if annotation['id'] == -1:
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


@image_api.route('/api/image/<image_id>', methods=['GET'])
@login_required
def get_image_data(image_id):
    image = ensure_image_exists(image_id)
    if image is None:
        return jsonify({'message': 'there is no image with such an id'}), HTTPStatus.NOT_FOUND
    if not can_access_bank(image.image_bank, current_user):
        return jsonify({'message': 'not authorized to view this bank'}), HTTPStatus.UNAUTHORIZED
    next_image = db.session.query(ImageToAnnotate)\
        .filter(and_(ImageToAnnotate.image_bank_id == image.image_bank_id,
                     ImageToAnnotate.id > image.id))\
        .order_by(ImageToAnnotate.id)\
        .first()
    prev_image = db.session.query(ImageToAnnotate)\
        .filter(and_(ImageToAnnotate.image_bank_id == image.image_bank_id,
                     ImageToAnnotate.id < image.id))\
        .order_by(desc(ImageToAnnotate.id))\
        .first()
    
    # auto keywords
    keywords = get_keywords(image.description)
    
    return jsonify({
        'id': image.id,
        'description': image.description,
        'width': image.width,
        'height': image.height,
        'imageUrl':  'image-serve/' + image.file_url,
        'hasNext': next_image.id if next_image is not None else -1,
        'hasPrevious': prev_image.id if prev_image is not None else -1,
        'annotations': [
            {
                'tag': annotation.tag,
                'regionInfo': annotation.region_info,
                'author': annotation.author.username,
            }
            for annotation in image.annotations
        ],
        'keywords': keywords,
    })


@image_api.route('/api/image/annotations/<image_id>', methods=['GET'])
@login_required
def get_annotations(image_id):
    """
    Returns the annotations of the image with id `image_id`.
    """
    image = ensure_image_exists(image_id)
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


@image_api.route('/api/image-serve/<path:path>')
def serve_image(path):
    if path:
        return send_file(os.path.join(default_bank_directory, path), mimetype='image/jpeg')
    return jsonify({'message': 'no such image'}), HTTPStatus.NOT_FOUND
