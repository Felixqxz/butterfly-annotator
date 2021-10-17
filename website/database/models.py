from sqlalchemy.orm import relationship
from .access import db

class User(db.Model):
    """
    Represents an app's user.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String())

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def get_user(user_id):
        if user_id is None:
            return None
        # TODO

class ImageBank(db.Model):
    """
    Represents a bank of images to annotate.
    """
    __tablename__ = 'image_bank'

    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(25), unique=True)
    images = relationship('ImageToAnnotate', back_populates='image_bank')

    def __init__(self, bank_name):
        self.bank_name = bank_name

    def __repr__(self):
        return '<ImageBank %r>' % self.bank_name

class ImageToAnnotate(db.Model):
    """
    Represents an image to annotate.
    """
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    image_bank_id = db.Column(db.Integer, db.ForeignKey('image_bank.id'))
    image_bank = relationship('ImageBank', back_populates='images')
    # The URL contains the filename which also serves as a name to the image
    file_url = db.Column(db.String(), unique=True)
    width = db.Column(db.SmallInteger)
    height = db.Column(db.SmallInteger)
    annotations = relationship('ImageAnnotation', back_populates='annotation.image')

    def __init__(self, image_bank_id, file_url, width, height):
        self.image_bank_id = image_bank_id
        self.file_url = file_url
        self.width = width
        self.height = height

class ImageAnnotation(db.Model):
    """
    Represents an annotation on an `ImageToAnnotate`.
    """
    __tablename__ = 'annotation'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    tag = db.Column(db.String())
    region_info = db.Column(db.String())
    image = relationship('ImageToAnnotate', back_populates='annotations')

    def __init__(self, image_id, tag, region_info):
        self.image_id = image_id
        self.tag = tag
        self.region_info = region_info
