"""
The part of the API that allows access to the images of a database.
"""
from flask.json import jsonify

def list_images_setup(app):
    assert app is not None
    @app.route('/api/dir/<bank>', methods=['GET'])
    def list_images(bank):
        return jsonify({'bank': bank}) # TODO
