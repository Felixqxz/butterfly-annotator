"""
The part of the API that allows access to the images of a database.
"""
from operator import methodcaller
from flask.json import jsonify
from flask import Blueprint, request
from flask_login import login_required, current_user
from http import HTTPStatus
import os
from ..database.access import db
from ..database.models import BankAccess

basedir = os.path.abspath(os.path.dirname(__name__))
bank_api = Blueprint('bank_api', __name__)


# This route allows to fetch the list of banks a user can see.
@bank_api.route('/api/bank-list', methods=['GET'])
@login_required
def list_banks():
    banks = []
    for access in current_user.accesses:
        banks.append({
            'id': access.bank.id,
            'name': access.bank.bankname,
            'description': access.bank.description
        })
    return jsonify(banks)

# This route is used to add a bank.
@bank_api.route('/api/bank/add/', methods=['POST'])
@login_required
def add_bank():
    method = request.method
    bank = request.json.get('bankFile')

    if not bank:
        return 'No bank added', HTTPStatus.BAD_REQUEST

    new_bank = BankAccess(user_id= bank.user_id, bank_id= bank.bank_id)

    db.session.add(new_bank)
    db.session.commit()

    return jsonify({
        'bank_id': bank.bank_id,
        'method': method
    })

# This api is used to delete a bank
@bank_api.route('/api/bank/delete/', methods=['POST'])
def delete_bank():
    bank_id = request.json.get('bank_id')
    bank = BankAccess.query.filter_by(id=bank_id).first()

    if bank:
        db.session.delete(bank)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': 'bank deleted!',
        })
    else:
        return jsonify({
            'status': 401,
            'message': 'bank not found'
        })
