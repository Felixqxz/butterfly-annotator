"""
The part of the API that allows access to the images of a database.
"""
from operator import methodcaller
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

# This route allows to fetch the list of images of a given bank.
@image_api.route('/api/bank/<bank_id>', methods=['GET'])
@login_required
def list_images(bank_id):
    if not bank_id.isnumeric():
        return jsonify({'error': 'ill-formed request'}), HTTPStatus.BAD_REQUEST
    banks_dict = {
        access.bank_id: access.bank for access in current_user.accesses}
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






# This route is used to upload an folder.
# @image_api.route('/api/upload/folder', methods=['POST'])
# @login_required
# def upload_folder():
#     # TODO: fix this here; might remove this whole endpoint
#     method = request.method
#     pic = request.files['imgFile']

#     if not pic:
#         return 'No pic uploaded', HTTPStatus.BAD_REQUEST

#     path = basedir + '/website/static/source_images/'
#     file_path = path + pic.filename
#     pic.save(file_path)

#     image_bank_id = 1
#     # TODO convert to path relative to the folder containing the banks
#     file_url = '../../../website/static/source_images/' + pic.filename

#     image_to_annotate = ImageToAnnotate(image_bank_id=image_bank_id, file_url=file_url)
#     db.session.add(image_to_annotate)
#     db.session.commit()

#     return jsonify({
#         'image_bank_id': image_bank_id,
#         'image_name': pic.filename,
#         'method': method
#     })

# This route is used to upload multiple images.
@image_api.route('/api/upload/multiple/images', methods=['POST'])
def upload_multiple_images():
    # TODO: fix this here; might remove this whole endpoint
    method = request.method
    pics = request.files.getlist('images')
    # print(request.files.count)
    print(pics)
    if not pics:
        return 'No pic uploaded', HTTPStatus.BAD_REQUEST

    # print(pics)

    for pic in pics:
        path = basedir + '/website/static/source_images/'
        file_path = path + pic.filename
        pic.save(file_path)

        image_bank_name = pic.bank_name
        file_url = '../../../website/static/source_images/' + pic.filename

        image_to_annotate = ImageToAnnotate(image_bank_name=image_bank_name, file_url=file_url)
        db.session.add(image_to_annotate)
        db.session.commit()


    return jsonify({
            'status': 200})


    # return jsonify({
    #     'image_bank_id': image_bank_id,
    #     'image_name': pic.filename,
    #     'method': method
    # })


# This route allows to get the image information
@image_api.route('/api/image/<image_id>', methods=['GET'])
@login_required
def get_image(image_id):
    image = db.session.query(ImageToAnnotate).filter(
        ImageToAnnotate.id == image_id).first()
    if image is None:
        return jsonify({'message': 'image not found'}), HTTPStatus.NOT_FOUND

    return {
        'image': {
            'id': image.id,
            'url': image.file_url,
            'description': image.description,
            'width': image.width,
            'height': image.height
        }
    }

# This route allows to get the next image in the same image bank
@image_api.route('/api/image/next/<image_id>', methods=['GET'])
@login_required
def get_next_image(image_id):
    image = db.session.query(ImageToAnnotate).filter(
        ImageToAnnotate.id == image_id).first()
    bank_id = image.image_bank_id

    banks_dict = {
        access.bank_id: access.bank for access in current_user.accesses}

    next_image = db.session.query(ImageToAnnotate).filter(ImageToAnnotate.image_bank_id == bank_id,
                                                          ImageToAnnotate.id > image_id).first()
    if next_image is None:
        return jsonify({
            'status': 404,
            'message': 'no next image'})

    next_image_id = next_image.id
    return {
        'status': 200,
        'image': {
            'id': next_image.id,
            'url': next_image.file_url,
            'description': next_image.description
        }
    }

# This route allows to get the previous image in the same image bank


@image_api.route('/api/image/previous/<image_id>', methods=['GET'])
@login_required
def get_previous_image(image_id):
    image = db.session.query(ImageToAnnotate).filter(
        ImageToAnnotate.id == image_id).first()
    bank_id = image.image_bank_id

    previous_image = db.session.query(ImageToAnnotate).filter(ImageToAnnotate.image_bank_id == bank_id,
                                                              ImageToAnnotate.id < image_id).order_by(ImageToAnnotate.id.desc()).first()
    if previous_image is None:
        return jsonify({
            'status': 404,
            'message': 'no previous image'})

    return {
        'status': 200,
        'image': {
            'id': previous_image.id,
            'url': previous_image.file_url,
            'description': previous_image.description
        }

    }


# This route is used to upload an image.
@image_api.route('/api/image/upload', methods=['POST'])
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

    image_to_annotate = ImageToAnnotate(
        image_bank_id=image_bank_id, file_url=file_url)
    db.session.add(image_to_annotate)
    db.session.commit()

    return jsonify({
        'image_bank_id': image_bank_id,
        'image_name': pic.filename,
        'method': method
    })

# This api is used to get all images info that user uploaded
@image_api.route('/api/image/delete/', methods=['POST'])
def delete_image():
    image_id = request.json.get('image_id')
    image = ImageToAnnotate.query.filter_by(id=image_id+1).first()

    if image:
        db.session.delete(image)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': 'image deleted!',
            'image': image.image_name
        })
    else:
        return jsonify({
            'status': 401,
            'message': 'image not found'
        })



# This route is used to get all images info that user uploaded.
@image_api.route('/api/image/getImage', methods=['GET'])
@login_required
def get_images():
    images = []
    count = ImageToAnnotate.query.filter_by(image_bank_id=1).count()
    for i in range(count):
        image = ImageToAnnotate.query.filter_by(
            id=i + 1).first()  # TODO: what is this?
        images.append({
            'id': i,
            'url': image.file_url,
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
    image_id = int(req['image_id'])
    image_query = db.session.query(ImageToAnnotate).filter(
        ImageToAnnotate.id == image_id)
    image = image_query.first()
    if image is None:
        return jsonify({'error': 'no such image'}), HTTPStatus.NOT_FOUND
    if 'annotations' not in req:
        return jsonify({'result': 'success'})
    if image.image_bank.id not in [access.bank_id for access in current_user.accesses]:
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
            a = ImageAnnotation(image.id, stripped_tag,
                                region.sql_serialize_region())
            db.session.add(a)
        else:
            db.session.query(ImageAnnotation)\
                .filter(ImageAnnotation.id == int(annotation['id']))\
                .update({
                    ImageAnnotation.region_info: region.sql_serialize_region(),
                    ImageAnnotation.tag: stripped_tag
                })
    return jsonify({'result': 'success'})
