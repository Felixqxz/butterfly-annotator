from flask import Flask, json, jsonify
from flask_cors import CORS
from .database.access import db
from .config import config_by_name

# configuration
DEBUG = True

def create_app(config_name=None):
    # create and configure the app
    app = Flask(__name__)

    if config_name is None:
        app.config.from_object(config_by_name['default'])
    else:
        app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # sanity check route
    @app.route('/', methods=['GET'])
    def ping_pong():
        return jsonify('Hello World!')

    from .images.image_api import image_api
    app.register_blueprint(image_api)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
