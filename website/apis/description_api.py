"""
The part of the API that allows access to the decriptions of a database.
"""
from __future__ import print_function # In python 2.7

from flask.json import jsonify
from flask import Blueprint, request, make_response, Response
import os

from sqlalchemy.util.langhelpers import counter
from ..database.access import db
from flask_cors import cross_origin
from ..database.models import Description

import sys

basedir = os.path.abspath(os.path.dirname(__name__))
description_api = Blueprint('description_api', __name__)

@description_api.route('/button/')
def button_clicked():
    print('Hello world!', file=sys.stderr)
    return redirect('/')

@description_api.route('/api/description/upload', methods=['POST', 'GET'])
def upload_description():

    method = request.method
    #print(list(request.files.keys())[0])

    text = request.files['txtFile']
    #print(text.read())

    if not text:
        return 'No description uploaded', 400

    
    path = basedir + "/website/static/source_descriptions/"
    file_path = path + text.filename
    text.save(file_path)  

    file_url = "../../../website/static/source_descriptions/" + text.filename
    description = Description(text = text.read(), file_url = file_url, description_name = text.filename, count = 1)
    db.session.add(description)
    db.session.commit()

    return jsonify({
        'status': 200,
        'description_name': text.filename,
        'method': method
    })

@description_api.route('/api/description/getDescription', methods=['GET'])
def get_description():
    ret = []
    count = Description.query.filter_by(count=1).count()
    for i in range(count):
        description = Description.query.filter_by(id=i+1).first()
        ret.append({
            'id': description.id,
            'url': description.file_url,
            'descriptionName': description.description_name,
            #'text' : description.text,
        })

    return jsonify({
        'status': 200,
        'descriptions': ret
    })
