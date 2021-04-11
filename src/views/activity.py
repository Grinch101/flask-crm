
from flask import Blueprint, request, make_response, g, jsonify
from src.models.activity import Activity
from src.models.contact import Contact
from utility.decor import login_required


phonebook = Contact()
activities = Activity()

activity = Blueprint('activity', __name__)

@activity.route('/<int:contact_id>', methods=["GET"])
@login_required
def get_all(contact_id):

    contact_name = phonebook.get_by_id(contact_id)['name']
    cur = activities.get_all(contact_id)

    return make_response( jsonify( {'contact_name':contact_name}, {'data':cur.fetchall()} ) , 200 )


@activity.route('/<int:contact_id>', methods=["POST"])
@login_required
def add(contact_id):

    action = request.form['action']
    description = request.form['description']
    date = request.form['date']
    time = request.form['time']

    activities.add(action, description, date, time,
                   g.user['id'], contact_id)

    return make_response(jsonify('activity added'), 201)


@activity.route('/<int:contact_id>/delete/<int:activity_id>', methods=["DELETE"])
@login_required
def delete(contact_id, activity_id):

    if activities.delete(activity_id):
        return make_response(jsonify('activity deleted!'), 200)
    else:
        return make_response(jsonify(f'activity id {activity_id} was not found in the database'), 404)
