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
    has_profile_picture = db.Column(db.Boolean)

    accesses = relationship('BankAccess', back_populates='user')
    annotations = relationship('ImageAnnotation', back_populates='author')

    def __init__(self, username, email, password_hash, has_profile_picture=False):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.has_profile_picture = has_profile_picture

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
    keywords = relationship('UserSelectedKeyword', back_populates='image_bank')

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bank_id = db.Column(db.Integer, db.ForeignKey('image_bank.id'))
    permission_level = db.Column(db.SmallInteger)

    user = relationship('User', back_populates='accesses')
    bank = relationship('ImageBank', back_populates='accesses')

    def __init__(self, user_id, bank_id, permission_level):
        self.user_id = user_id
        self.bank_id = bank_id
        self.permission_level = permission_level

class ImageToAnnotate(db.Model):
    """
    Represents an image to annotate.
    """
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    image_bank_id = db.Column(db.Integer, db.ForeignKey('image_bank.id'))
    # path relative to the folder containing the banks
    file_url = db.Column(db.String())
    description = db.Column(db.String())
    # to avoid to have to fetch it each time from the file system
    width = db.Column(db.SmallInteger)
    height = db.Column(db.SmallInteger)

    image_bank = relationship('ImageBank', back_populates='images')
    annotations = relationship('ImageAnnotation', back_populates='image')

    def __init__(self, image_bank_id, file_url, description, width, height):
        self.image_bank_id = image_bank_id
        self.file_url = file_url
        self.description = description
        self.width = width
        self.height = height


class ImageAnnotation(db.Model):
    """
    Represents an annotation on an `ImageToAnnotate`.
    """
    __tablename__ = 'annotation'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    text_start = db.Column(db.SmallInteger)
    text_end = db.Column(db.SmallInteger)
    region_info = db.Column(db.String())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    image = relationship('ImageToAnnotate', back_populates='annotations')
    # The user responsible for this annotation
    author = relationship('User', back_populates='annotations')

    def __init__(self, image_id, text_start, text_end, region_info, author_id):
        self.image_id = image_id
        self.text_start = text_start
        self.text_end = text_end
        self.region_info = region_info
        self.author_id = author_id


class UserSelectedKeyword(db.Model):
    """
    Represents user-selected keywords.
    """
    __tablename__ = 'user_keywords'

    id = db.Column(db.Integer, primary_key=True)
    image_bank_id = db.Column(db.Integer, db.ForeignKey('image_bank.id'))
    keyword = db.Column(db.String())

    image_bank = relationship('ImageBank', back_populates='keywords')

    def __init__(self, image_bank_id, keyword):
        self.image_bank_id = image_bank_id
        self.keyword = keyword
