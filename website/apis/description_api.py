"""
The part of the API that allows access to the decriptions of a database.
"""
from __future__ import print_function # In python 2.7

from flask.json import jsonify
from flask import Blueprint, request, make_response, Response, flash
import os
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

    
    #print(list(request.files.keys())[0])

    text = request.files['txtFile']
    #print(text.read())

    if not text:
        return 'No description uploaded', 400

    '''
    path = basedir + "/website/static/description_files/"
    file_path = path + text.filename
    text.save(file_path)  
    '''

    # There may be some issues with database
    

    description = Description(text = text.read())
    db.session.add(description)
    db.session.commit()

    return 'Description has been uploaded', 200

@description_api.route('/api/description/getDescription', methods=['GET'])
def get_description():
    description = Description.query.filter_by(id=id).first()
    if not description:
        return 'No description with that id', 404
    
    '''
    response = make_response(description.)
    response.headers['Content-Type'] = 'image/png'

    return Response(img.img)
    '''
