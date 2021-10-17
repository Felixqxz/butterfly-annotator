"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify
from flask import Blueprint, request, make_response
from ..database.access import db
from ..database.models import ImageAnnotation, ImageToAnnotate
from ..images.geometry import PolygonalRegion

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


@image_api.route('/api/image/annotate', methods=['PUT'])
def insert_annotation():
    """
    Allows to push all the annotations of the image to the database.
    """
    req = request.get_json()
    image_id = int(req['image_id'])
    image_query = db.session.query(ImageToAnnotate).filter(ImageToAnnotate.id == image_id)
    image = image_query.first()
    if image is None:
        return make_response(jsonify({'error': 'no such image'}), 404)
    if 'annotations' not in req:
        return make_response(jsonify({'message': 'success'}))
    # first pass: verify all data
    for annotation in req['annotations']:
        try:
            region = PolygonalRegion(annotation['points'])
        except Exception:
            return make_response(jsonify({'error': 'ill-formed polygonal region'}), 400)
        if max(map(lambda p: p.x, region.points)) > image.width or \
                min(map(lambda p: p.x, region.points)) < 0 or \
                max(map(lambda p: p.y, region.points)) > image.height or \
                min(map(lambda p: p.y, region.points)) < 0:
            return make_response(jsonify({'error': 'there exists a point out of bounds'}), 400)
        if annotation['id'] != '-1':
            # trying to update existing annotation
            if int(annotation['id']) not in [annot.id for annot in image.annotations]:
                return make_response(jsonify({'error': 'trying to update an annotation that does not exist'}), 400)

    # second pass: update database
    for annotation in req['annotations']:
        region = PolygonalRegion(annotation['points'])
        stripped_tag = annotation['tag'].strip().tolower()
        if annotation['id'] == '-1':
            # new region
            a = ImageAnnotation(image.id, stripped_tag, region.sql_serialize_region())
            db.session.add(a)
        else:
            db.session.query(ImageAnnotation)\
                .filter(ImageAnnotation.id == int(annotation['id']))\
                .update({
                    ImageAnnotation.region_info: region.sql_serialize_region(),
                    ImageAnnotation.tag: stripped_tag
                })
    return jsonify({'result': 'success'})
