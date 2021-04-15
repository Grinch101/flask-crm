from flask import Blueprint, make_response, g, jsonify, request
from src.models.contact import Contact
from utility.decor import login_required
from utility.helpers import JSON_output
from psycopg2 import errors

phonebook = Contact()

contact = Blueprint('contact', __name__)

@contact.route('/', methods=["GET"])
@login_required
def index():
    # I think this handler is of no use as well! should I drop it?
    output = JSON_output(message='index page', g=g, cur= None)
    return make_response(output, 200)


@contact.route('/add', methods=["POST"])
@login_required
def add():

    input_name = request.form['Name']
    input_number = request.form['Number']
    cur = phonebook.add(g.user['id'], input_name, input_number)
    output = JSON_output(message='contact added!', g=g, cur=cur)

    return make_response(output, 201)


@contact.route('/all', methods=["GET"])
@login_required
def get_all():

    cur = phonebook.get_by_user(g.user['id'])
    output = JSON_output(message='All contacts retrieved!', g=g, cur=cur)

    return make_response(output , 200)


@contact.route('/delete/<int:id>', methods=["DELETE"])
@login_required
def delete(id):
    cur = phonebook.delete(id)
    if cur:
        output = JSON_output(message='contact deleted!', g=g, cur=cur)

        return make_response(output, 200)
    else:
        return make_response(jsonify(f'id {id} was not found in the database') , 404)

