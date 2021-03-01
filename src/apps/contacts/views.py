from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, g
from models.contact import Contact
from utility.decor import login_required
from psycopg2 import errors

phonebook = Contact()

contact = Blueprint('contact', __name__)

@contact.route('/', methods=["GET"])
@login_required
def index():

    return render_template('index.html', username=g.user['client_name'])


@contact.route('/add', methods=["POST"])
@login_required
def add():

    input_name = request.form['Name']
    input_number = request.form['Number']
    phonebook.add(g.user['id'], input_name, input_number)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('contact.index'))


@contact.route('/all', methods=["GET"])
@login_required
def get_all():

    cur = phonebook.get_by_user(g.user['id'])

    return render_template('list.html', mylist=cur, username=g.user['client_name'])


@contact.route('/contacts/delete:<id>', methods=["POST"])
@login_required
def delete(id):
    phonebook.delete(id)
    flash(f"ID:{id} Deleted")

    return redirect(url_for('contact.get_all'))

