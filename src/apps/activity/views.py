
from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, g
from models.activity import Activity
from models.contact import Contact
from utility.decor import login_required


phonebook = Contact()
activities = Activity()

activity = Blueprint('activity', __name__)

@activity.route('/contact_id:<int:contact_id>', methods=["GET"])
@login_required
def get_all(contact_id):

    contact_name = phonebook.get_by_id(contact_id)['name']

    rows = activities.get_all(contact_id)

    return render_template('activity.html',
                           rows=rows,
                           contact_name=contact_name,
                           contact_id=contact_id,
                           username=g.user['client_name'])


@activity.route('/contact_id:<int:contact_id>', methods=["POST"])
@login_required
def add(contact_id):

    action = request.form['action']
    description = request.form['description']
    date = request.form['date']
    time = request.form['time']

    activities.add(action, description, date, time,
                   g.user['id'], contact_id)

    return redirect(url_for('activity.get_all', contact_id=contact_id))


@activity.route('/contact_id:<int:contact_id>/delete:<int:activity_id>', methods=["POST"])
@login_required
def delete(contact_id, activity_id):

    activities.delete(activity_id, contact_id)

    return redirect(url_for('activity.get_all', contact_id=contact_id))
