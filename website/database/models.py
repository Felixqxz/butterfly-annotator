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

class ImageBank(db.Model):
    """
    Represents a bank of images to annotate.
    """
    __tablename__ = 'image_bank'

    id = db.Column(db.Integer, primary_key=True)
    bankname = db.Column(db.String(25), unique=True)
    images = relationship('ImageToAnnotate', back_populates='image_bank')

    def __init__(self, bankname):
        self.bankname = bankname

    def __repr__(self):
        return '<ImageBank %r>' % self.bankname

class ImageToAnnotate(db.Model):
    """
    Represents an image to annotate.
    """
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    image_bank_id = db.Column(db.Integer, db.ForeignKey('image_bank.id'))
    image_bank = relationship('ImageBank', back_populates='images')
    file_url = db.Column(db.String())
