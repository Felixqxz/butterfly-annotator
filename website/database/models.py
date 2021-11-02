from sqlalchemy.orm import relationship
from .access import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """
    Represents an app's user.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String())

    accesses = relationship('BankAccess', back_populates='user')

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '<User %r>' % self.username

class ImageBank(db.Model):
    """
    Represents a bank of images to annotate.
    """
    __tablename__ = 'image_bank'

    id = db.Column(db.Integer, primary_key=True)
    bankname = db.Column(db.String(25), unique=True)
    description = db.Column(db.String(150))

    images = relationship('ImageToAnnotate', back_populates='image_bank')
    accesses = relationship('BankAccess', back_populates='bank')

    def __init__(self, bankname, description):
        self.bankname = bankname
        self.description = description

    def __repr__(self):
        return '<ImageBank %r>' % self.bankname

class BankAccess(db.Model):
    """
    Represents an access of a user to a bank. If an entry
    for a certain user and bank does not exist, then user cannot access.
    Note: We might want to allow different bank visibility levels.
    """
    __tablename__ = 'bank_access'

    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(25), db.ForeignKey('user.username'))
    bank_name = db.Column(db.String(25), db.ForeignKey('image_bank.bankname'))
    # TODO define what int defines what level of privilege
    # permission_level = db.Column(db.SmallInteger)

    user = relationship('User', back_populates='accesses')
    bank = relationship('ImageBank', back_populates='accesses')

    def __init__(self, user_name, bank_name):
        self.user_name = user_name
        self.bank_name = bank_name
        # self.permission_level = permission_level

class ImageToAnnotate(db.Model):
    """
    Represents an image to annotate.
    """
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    image_bank_name = db.Column(db.String(25), db.ForeignKey('image_bank.bankname'))
    # path relative to the folder containing the banks
    file_url = db.Column(db.String())
    description = db.Column(db.String())
    # to avoid to have to fetch it each time from the file system
    width = db.Column(db.SmallInteger)
    height = db.Column(db.SmallInteger)

    image_bank = relationship('ImageBank', back_populates='images')
    annotations = relationship('ImageAnnotation', back_populates='image')

    def __init__(self, image_bank_name, file_url, description, width, height):
        self.image_bank_id = image_bank_name
        self.file_url = file_url
        self.description = description
        self.width = width
        self.height = height

    def __init__(self, image_bank_name, file_url):
        self.image_bank_id = image_bank_name
        self.file_url = file_url


class Description(db.Model):
    """
    Represents an image to annotate.
    """
    __tablename__ = 'description'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    # TODO: change this, it should not be done this way (probably) => handle in ImageToAnnotate


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
