import json
from flask import Blueprint, g, request
from src.models.contact import Contact
from utility.decor import login_required
from utility.helpers import json_output

phonebook = Contact()

contact = Blueprint('contact', __name__)


@contact.route('/', methods=["GET"])
@login_required
def index():
    # I think this handler is of no use as well! should I drop it?
    return json_output(message='index page')


@contact.route('/add', methods=["POST"])
@login_required
def add():

    input_name = request.form['Name']
    input_number = request.form['Number']
    if not all([input_name, input_number]):
        return json_output(error='incomplete request!', http_code=401)
    else:
        cur = phonebook.add(g.user['id'], input_name, input_number)
        data = cur.fetchall()
        return json_output(message='contact added!', data=data, http_code=201)


@contact.route('/all', methods=["GET"])
@login_required
def get_all():

    cur = phonebook.get_by_user(g.user['id'])
    if cur:
        data = cur.fetchall()
        return json_output(message='All contacts retrieved!', data=data)
    else:
        return json_output(error='user not found!', http_code=404)


@contact.route('/delete/<int:id>', methods=["DELETE"])
@login_required
def delete(id):
    cur = phonebook.delete(id)
    if cur:
        data = cur.fetchone()
        return json_output(message='contact deleted!', data=data)

    else:
        return json_output(error='user was not found!', http_code=404)


@contact.route('/update/<int:id>', methods=['PUT'])
@login_required
def update(id):
    if request.form is not None:
        
        new_name = request.form('new_name')
        new_phone = request.form('new_phone')
        update_keys = list(dict(request.form).keys())
        update_vals = [new_name, new_phone]
        cur = phonebook.update(g.user['id'],id, update_keys, update_vals)
        if cur:
            data = cur.fetchall()
            return json_output(message='updated!', data = data) 
        else:
            if not cur[0] and cur[1] == '400':
                json_output(error='Bad Request!', http_code= 400) # Bad request!
            if not cur[0] and cur[1] == '401':
                json_output(error='Unauthorized!', http_code= 401) # Unauthorized!
    else: 
        return json_output(error='Empty Request!', http_code= 400) # Bad request!


