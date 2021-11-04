import os
import glob
from pathlib import Path
from ..database.models import ImageBank, ImageToAnnotate, BankAccess, User
from ..database.access import db
from PIL import Image

base_directory = os.getcwd()
default_bank_directory = base_directory + os.sep + 'banks'
BANK_DESCRIPTION_FILE = 'description.txt'


def discover_all_banks():
    if not os.path.isdir(default_bank_directory):
        os.mkdir(default_bank_directory)
    bank_list = glob.glob(default_bank_directory + os.sep + '*' + os.sep)
    for bank in bank_list:
        print('> discovering bank ' + bank)
        discover_bank(bank)


def discover_bank(bank_path):
    # first, get bank's description
    bank_description = ''
    bank_name = os.path.basename(os.path.normpath(bank_path))
    q = db.session.query(ImageBank).filter(ImageBank.bankname == bank_name).first()
    if q is not None:
        print('!> bank ' + bank_name + ' already exists')
        return
    desc_file_path = os.path.join(bank_path, BANK_DESCRIPTION_FILE)
    # if has description file
    if os.path.isfile(desc_file_path):
        with open(desc_file_path, 'r') as file:
            bank_description = file.read().replace('\n', '')
        print('>> found description.txt')
    # list images
    all_images = glob.glob(bank_path + '/*.jpg')
    all_pairs = []
    for image in all_images:
        # find matching description
        name_no_ext = Path(image).stem
        splits = name_no_ext.split('_')
        if len(splits) > 2:
            # ignore masks, for now
            continue
        print('>> found image ' + name_no_ext)
        data_description_file = os.path.join(bank_path, splits[0] + '.txt')
        if not os.path.isfile(data_description_file):
            print('!> could not find a description for image ' + name_no_ext + '.jpg')
            # no description available! skip
            continue
        # matching description found, read it, and add it to list
        txt_description = ''
        with open(data_description_file, 'r') as file:
            txt_description = file.read()
        all_pairs.append({
            'path': os.path.join(bank_path, name_no_ext + '.jpg'),
            'name': bank_name + os.sep + name_no_ext + '.jpg',
            'description': txt_description,
        })
    # now that we have all images, push them to the database
    # first, create bank
    bank = ImageBank(bank_name, bank_description)
    db.session.add(bank)
    db.session.commit()
    for pair in all_pairs:
        img_file = Image.open(pair['path'])
        width, height = img_file.size
        img = ImageToAnnotate(bank.id, pair['name'], pair['description'], width, height)
        db.session.add(img)
    db.session.commit()
    # + give access to admin by default
    admin = db.session.query(User).filter(User.username == 'admin').first()
    db.session.add(BankAccess(admin.id, bank.id, 100))
    db.session.commit()
    print('>> done!')
