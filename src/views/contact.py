from flask import Blueprint, make_response, g, jsonify, request
from src.models.contact import Contact
from utility.decor import login_required
from psycopg2 import errors

phonebook = Contact()

contact = Blueprint('contact', __name__)

@contact.route('/', methods=["GET"])
@login_required
def index():
    username=g.user['client_name']
    return make_response( jsonify(f'index page for user: ->{username}<-') , 200)


@contact.route('/add', methods=["POST"])
@login_required
def add():

    input_name = request.form['Name']
    input_number = request.form['Number']
    phonebook.add(g.user['id'], input_name, input_number)

    return make_response(jsonify(f'{input_name}, {input_number} added'), 201)


@contact.route('/all', methods=["GET"])
@login_required
def get_all():

    cur = phonebook.get_by_user(g.user['id'])
    return make_response( jsonify ( cur.fetchall()) , 200)


@contact.route('/delete/<int:id>', methods=["DELETE"])
@login_required
def delete(id):

    if phonebook.delete(id):
        return make_response(jsonify(f'Entity deleted {id}'), 200)
    else:
        return make_response( jsonify(f'id {id} was not found in the database') , 404)

