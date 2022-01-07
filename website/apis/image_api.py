"""
The part of the API that allows access to the images of a database.
"""
from pathlib import Path
from flask.json import jsonify
from flask import Blueprint, request, escape, send_file
from flask_login import login_required, current_user
from sqlalchemy import and_, desc
from http import HTTPStatus
import os
import shutil
import zipfile

from website.images.banks import delete_bank
from ..database.access import db
from ..database.models import User, BankAccess, ImageToAnnotate, ImageAnnotation, ImageBank, UserSelectedKeyword
from ..images.geometry import PolygonalRegion
from ..images.discovery import default_bank_directory, discover_bank
from ..textproc.proc import get_keywords

basedir = os.path.abspath(os.path.dirname(__name__))
image_api = Blueprint('image_api', __name__)


ADJ_LIST_PATH = os.path.join(os.getcwd(), 'termlist', 'adjlist.txt')
COLOR_LIST_PATH = os.path.join(os.getcwd(), 'termlist', 'colorlist.txt')
PATTERN_LIST_PATH = os.path.join(os.getcwd(), 'termlist', 'patternlist.txt')


bank_access_levels = {
    'super-admin': 100,  # reserved: one such account per app instance
    'admin': 90,
    'moderator': 70,  # allows to annotate and manage other editors/viewers
    'editor': 50,  # only allows to annotate
    'viewer': 0,
}


def load_word_list(p):
    """
    Loads a list of provided words.
    """
    ls = []
    if os.path.isfile(p):
        with open(p, 'r') as file:
            lines = file.readlines()
            for line in lines:
                ls.append(line.strip().lower())
    return ls


# lists of words for the automatic suggestions
adj_list = load_word_list(ADJ_LIST_PATH) + load_word_list(COLOR_LIST_PATH)
pattern_list = load_word_list(PATTERN_LIST_PATH)


def gen_annotation_array(image):
    return [
        {
            'id': annotation.id,
            'description': {
                'start': annotation.text_start,
                'end': annotation.text_end,
            },
            'regionInfo': annotation.region_info,
        } for annotation in image.annotations
    ]


def save_user_keywords_selection(description, image_bank_id, start, end):
    """
    Adds user's provided selection to the database for future suggestions.
    """
    words = description[start:end].lower()
    keyword = db.session.query(UserSelectedKeyword)\
        .filter(and_(UserSelectedKeyword.image_bank_id == image_bank_id, UserSelectedKeyword.keyword == words))\
        .first()
    if not keyword:
        user_selected_keyword = UserSelectedKeyword(image_bank_id=image_bank_id, keyword=words)
        db.session.add(user_selected_keyword)
        db.session.commit()


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


@image_api.route('/api/bank-access', methods=['PUT'])
@login_required
def manage_access_bank():
    data = request.get_json()
    if 'id' not in data or 'targetName' not in data or 'level' not in data:
        return jsonify({'message': 'missing field'}), HTTPStatus.BAD_REQUEST
    if not data['id'].isnumeric():
        return jsonify({'message': 'invalid bank id'}), HTTPStatus.BAD_REQUEST
    level = data['level']
    if level < -1 or level > 90:
        # the maximal assignable level is admin (super-admin is reserved)
        return jsonify({'message': 'invalid permission level'}), HTTPStatus.UNAUTHORIZED
    # search target user
    target_user = db.session.query(User).filter(User.username == escape(data['targetName'])).first()
    if target_user is None:
        return jsonify({'message': 'no such target user'}), HTTPStatus.NOT_FOUND
    bank = db.session.query(ImageBank).filter(ImageBank.id == int(data['id'])).first()
    if bank is None:
        return jsonify({'message': 'no such bank'}), HTTPStatus.NOT_FOUND
    user_access = get_bank_access_level(current_user, bank.id)
    if not user_access:
        return jsonify({'message': 'you do not have access to this bank'}), HTTPStatus.UNAUTHORIZED
    # now that bank & target exist and are accessible,
    # check for permission levels
    if user_access.permission_level < bank_access_levels['moderator']:
        return jsonify({'message': 'insufficient permissions'}), HTTPStatus.UNAUTHORIZED
    if level >= bank_access_levels['moderator'] and user_access.permission_level < user_access['admin']:
        # only admins can assign other admins and moderators
        return jsonify({'message': 'insufficient permissions'}), HTTPStatus.UNAUTHORIZED
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
    return jsonify({'message': 'insufficient permissions'}), HTTPStatus.UNAUTHORIZED


@image_api.route('/api/bank-list-accesses/<bank_id>', methods=['GET'])
@login_required
def list_bank_accesses(bank_id):
    if not bank_id.isnumeric():
        return jsonify({'message': 'invalid bank id'}), HTTPStatus.BAD_REQUEST
    bank = db.session.query(ImageBank).filter(ImageBank.id == int(bank_id)).first()
    if bank is None:
        return jsonify({'message': 'no such bank'}), HTTPStatus.NOT_FOUND
    if not can_access_bank(bank, current_user):
        return jsonify({'message': 'you do not have access to this bank'}), HTTPStatus.UNAUTHORIZED
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
        return jsonify({'message': 'ill-formed request'}), HTTPStatus.BAD_REQUEST
    banks_dict = {access.bank_id: access.bank for access in current_user.accesses}
    bank_id = int(bank_id)
    if bank_id not in banks_dict:
        return jsonify({'message': 'you do not have access to this bank'}), HTTPStatus.UNAUTHORIZED
    return {
        'bankName': banks_dict[bank_id].bankname,
        'images': [
            {
                'id': image.id,
                'url': 'image-serve/' + image.file_url,
                'fullDescription': image.description,
                'lastEditor': {
                    'username': image.annotations[0].author.username,
                } if image.annotations else '',
            } for image in banks_dict[bank_id].images
        ]}


@image_api.route('/api/image/annotate', methods=['POST'])
@login_required
def insert_annotations():
    """
    Allows to push all the annotations of the image to the database.
    Returns the ids in the order of insertion.
    """
    req = request.get_json()
    image = ensure_image_exists(req['imageId'])
    if image is None:
        return jsonify({'message': 'there exists no image with such an id'}), HTTPStatus.NOT_FOUND
    if 'annotations' not in req:
        return jsonify({'result': 'success'})
    if not can_access_bank(image.image_bank, current_user, access_level='editor'):
        return jsonify({'message': 'not authorized to annotate this bank'}), HTTPStatus.UNAUTHORIZED
    # first pass: verify all data
    for annotation in req['annotations']:
        if annotation['id'] != -1:
            # trying to update existing annotation
            if int(annotation['id']) not in [annot.id for annot in image.annotations]:
                return jsonify({'message': 'trying to update an annotation that does not exist'}), \
                       HTTPStatus.BAD_REQUEST
        if 'rem' in annotation:
            continue
        try:
            region = PolygonalRegion.deserialize_from_json(annotation['points'])
        except Exception:
            return jsonify({'message': 'ill-formed polygonal region'}), HTTPStatus.BAD_REQUEST
        if max(map(lambda p: p.x, region.points)) > image.width or \
                min(map(lambda p: p.x, region.points)) < 0 or \
                max(map(lambda p: p.y, region.points)) > image.height or \
                min(map(lambda p: p.y, region.points)) < 0:
            return jsonify({'message': 'there exists a point out of bounds'}), HTTPStatus.BAD_REQUEST

    # second pass: update database
    ids = []
    for annotation in req['annotations']:
        if 'rem' in annotation:
            db.session.query(ImageAnnotation).filter(ImageAnnotation.id == annotation['id']).delete()
            db.session.commit()
        else:
            region = PolygonalRegion.deserialize_from_json(annotation['points'])
            start = annotation['tag']['start']
            end = annotation['tag']['end']
            if annotation['id'] == -1:
                # new region
                a = ImageAnnotation(image.id, start, end, region.sql_serialize_region(), current_user.get_id())
                db.session.add(a)
                # commit now to get proper ID
                db.session.commit()
                ids.append(a.id)

                # save annotations to user_keyword_selection file
                save_user_keywords_selection(image.description, image.image_bank_id, start, end)
            else:
                existing_annotation = db.session.query(ImageAnnotation)\
                    .filter(ImageAnnotation.id == annotation['id']).first()
                if existing_annotation is None:  # Ignore: trying to update non existing
                    continue
                # no actual change to the data
                if existing_annotation.text_start != start or existing_annotation.text_end != end \
                    or PolygonalRegion.sql_serialize_region(region) == existing_annotation.region_info:
                    ids.append(annotation['id'])
                    continue
                # perform update
                db.session.query(ImageAnnotation)\
                    .filter(ImageAnnotation.id == annotation['id'])\
                    .update({
                        ImageAnnotation.region_info: region.sql_serialize_region(),
                        ImageAnnotation.text_start: start,
                        ImageAnnotation.text_end: end,
                        ImageAnnotation.author_id: current_user.get_id()
                    })
                db.session.commit()
                ids.append(annotation['id'])
    return jsonify({'result': 'success', 'ids': ids})


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
    return jsonify({
        'id': image.id,
        'bankId': image.image_bank.id,
        'description': image.description,
        'width': image.width,
        'height': image.height,
        'imageUrl':  'image-serve/' + image.file_url,
        'hasNext': next_image.id if next_image is not None else -1,
        'hasPrevious': prev_image.id if prev_image is not None else -1,
        'annotations': [
            {
                'id': annotation.id,
                'description': {
                    'start': annotation.text_start,
                    'end': annotation.text_end,
                },
                'regionInfo': annotation.region_info,
                'author': annotation.author.username,
            }
            for annotation in image.annotations
        ],
        # provide suggestions if the annotations list is empty
        'suggestions': get_keywords(adj_list, pattern_list, image.description,
                                    image.image_bank_id) if not image.annotations else '',
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
        'annotations': gen_annotation_array(image),
    })


@image_api.route('/api/image-serve/<path:path>')
def serve_image(path):
    if path:
        return send_file(os.path.join(default_bank_directory, path), mimetype='image/jpeg')
    return jsonify({'message': 'no such image'}), HTTPStatus.NOT_FOUND


@image_api.route('/api/bank/json/<int:bank_id>')
@login_required
def request_json(bank_id):
    bank = db.session.query(ImageBank).filter(ImageBank.id == bank_id).first()
    if bank is None:
        return jsonify({'message': 'no such bank'}), HTTPStatus.NOT_FOUND
    if not can_access_bank(bank, current_user):
        return jsonify({'message': 'you cannot view this bank'}), HTTPStatus.UNAUTHORIZED
    return {
        'id': bank.id,
        'name': bank.bankname,
        'description': bank.description,
        'images': [
            {
                'id': image.id,
                'description': image.description,
                'width': image.width,
                'height': image.height,
                'relativePath': image.file_url,
                'annotations': gen_annotation_array(image),
            }
            for image in bank.images
        ],
    }


@image_api.route('/api/bank/upload', methods=['POST'])
@login_required
def upload_bank():
    if not request.files:
        return jsonify({'message': 'no file provided'}), HTTPStatus.BAD_REQUEST
    archive = request.files['file']
    if not archive.filename.endswith('.zip'):
        return jsonify({'message': 'provided bank is not a zip archive'}), HTTPStatus.BAD_REQUEST
    location = os.path.join(default_bank_directory, archive.filename)
    bankname = Path(archive.filename).stem
    bank_loc = os.path.join(default_bank_directory, bankname)
    if os.path.isdir(bank_loc):
        return jsonify({'message': 'a bank having this name already exists'}), HTTPStatus.BAD_REQUEST
    os.mkdir(bank_loc)
    archive.save(location)
    with zipfile.ZipFile(location, 'r') as z:
        z.extractall(default_bank_directory)
    os.remove(location)
    new_bank, message = discover_bank(bank_loc)
    # could not add bank (eg nothing inside)
    if new_bank is None:
        shutil.rmtree(bank_loc)
        return jsonify({'message': message}), HTTPStatus.BAD_REQUEST
    # OK
    if current_user.username != 'admin':
        db.session.add(BankAccess(current_user.id, new_bank.id, bank_access_levels['admin']))
        db.session.commit()
    return jsonify({'message': message})


@image_api.route('/api/bank/delete/<int:bank_id>', methods=['GET'])
@login_required
def request_delete_bank(bank_id):
    bank = db.session.query(ImageBank).filter(ImageBank.id == bank_id).first()
    if bank is None or not can_access_bank(bank, current_user, access_level='admin'):
        return jsonify({'message': 'must be admin to delete a bank'}), HTTPStatus.UNAUTHORIZED
    delete_bank(bank)
    bank_loc = os.path.join(default_bank_directory, bank.bankname)
    if os.path.isdir(bank_loc):
        shutil.rmtree(bank_loc)
    return jsonify({'message': 'OK'})
