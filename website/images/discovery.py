import os
import glob
from pathlib import Path

from website.images.banks import delete_bank
from ..database.models import ImageBank, ImageToAnnotate, BankAccess, User
from ..database.access import db
from PIL import Image

base_directory = os.getcwd()
default_bank_directory = base_directory + os.sep + 'banks'
BANK_DESCRIPTION_FILE = 'description.txt'

def get_dimensions(path):
    img_file = Image.open(path)
    return img_file.size


def discover_all_banks():
    if not os.path.isdir(default_bank_directory):
        os.mkdir(default_bank_directory)
    bank_list = glob.glob(default_bank_directory + os.sep + '*' + os.sep)
    for bank in bank_list:
        print('> discovering bank ' + bank)
        discover_bank(bank)
    # now, delete banks that were removed by the user
    bank_names = [os.path.basename(os.path.normpath(bank_path)) for bank_path in bank_list]
    for bank in db.session.query(ImageBank).all():
        if bank.bankname not in bank_names:
            delete_bank(bank)
            print('> bank ' + bank.bankname + ' has been removed; deleted its entries in the database')


def discover_bank(bank_path):
    # first, get bank's description
    bank_description = ''
    bank_name = os.path.basename(os.path.normpath(bank_path))
    existing_bank = db.session.query(ImageBank).filter(ImageBank.bankname == bank_name).first()
    desc_file_path = os.path.join(bank_path, BANK_DESCRIPTION_FILE)
    # if has description file
    if os.path.isfile(desc_file_path):
        with open(desc_file_path, 'r') as file:
            bank_description = file.read().replace('\n', '')
        if existing_bank is not None and bank_description != existing_bank.description:
            existing_bank.description = bank_description
            db.session.commit()
            print('>> updated description of ' + bank_name)
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
        data_description_file = os.path.join(bank_path, splits[0] + '.txt')
        if not os.path.isfile(data_description_file):
            print('!> could not find a description for image ' + name_no_ext + '.jpg (skipping image)')
            # no description available! skip
            continue
        # matching description found, read it, and add it to list
        txt_description = ''
        with open(data_description_file, 'r') as file:
            txt_description = file.read()
        all_pairs.append({
            'path': os.path.join(bank_path, name_no_ext + '.jpg'),
            'name': bank_name + '/' + name_no_ext + '.jpg', # the file's relative location to the banks/ folder
            'description': txt_description.split('\n')[3], # the fourth line contains the description
        })
    print('>> found ' + str(len(all_images)) + ' image(s)')
    # now that we have all images, push them to the database
    if existing_bank is None:
        if not all_pairs:
            return None, 'No valid content found'
        # create the bank
        bank = ImageBank(bank_name, bank_description)
        db.session.add(bank)
        db.session.commit()
        # if the bank did not exist, then just add all images
        for pair in all_pairs:
            width, height = get_dimensions(pair['path'])
            img = ImageToAnnotate(bank.id, pair['name'], pair['description'], width, height)
            db.session.add(img)
        db.session.commit()
        # + give access to admin by default 
        admin = db.session.query(User).filter(User.username == 'admin').first()
        db.session.add(BankAccess(admin.id, bank.id, 100))
        db.session.commit()
        return bank, 'Found ' + str(len(all_pairs)) + ' images'
    else:
        # first, delete images that have been removed
        urls = [image['name'] for image in all_pairs]
        delete = [image for image in existing_bank.images if image.file_url not in urls]
        for d in delete:
            db.session.query(ImageToAnnotate).filter(ImageToAnnotate.file_url == d.file_url).delete()
        if delete:
            db.session.commit()
            print('>> deleted ' + str(len(delete)) + ' images')
        # now, add newer images
        existing_urls = [image.file_url for image in existing_bank.images]
        add = [image for image in all_pairs if image['name'] not in existing_urls]
        for a in add:
            width, height = get_dimensions(a['path'])
            db.session.add(ImageToAnnotate(existing_bank.id, a['name'], a['description'], width, height))
        if add:
            db.session.commit()
            print('>> added ' + str(len(add)) + ' images')
        return existing_bank, 'Found ' + str(len(all_pairs)) + ' images'
