
from flask import Blueprint, request, make_response, g, jsonify
from src.models.activity import Activity
from src.models.contact import Contact
from utility.decor import login_required
from utility.helpers import JSON_output


phonebook = Contact()
activities = Activity()

activity = Blueprint('activity', __name__)

@activity.route('/<int:contact_id>', methods=["GET"])
@login_required
def get_all(contact_id):

    cur = phonebook.get_by_id(contact_id)
    if cur:
        contact_name = cur['name']
        cur = activities.get_all(contact_id)
        if cur:
            output = JSON_output(message=f'All activity belong to user_id:{g.user["id"]} under its contact_id:{contact_id}',
                                g=g , cur=cur)

            return make_response(output , 200 )
        else:
            return make_response( jsonify('No activity found!') , 400 )
    else:
        return make_response( jsonify('Contact was not found!'), 404 )


@activity.route('/<int:contact_id>', methods=["POST"])
@login_required
def add(contact_id):

    action = request.form['action']
    description = request.form['description']
    date = request.form['date']
    time = request.form['time']

    cur = activities.add(action, description, date, time,
                   g.user['id'], contact_id)
    if cur:
        output = JSON_output(message='Activity Added!',g=g, cur=cur)

        return make_response(output, 201)
    else:
        return make_response(jsonify('contact was not found!') , 404)


@activity.route('/<int:contact_id>/delete/<int:activity_id>', methods=["DELETE"])
@login_required
def delete(contact_id, activity_id):
    cur = activities.delete(contact_id, activity_id)
    if cur:
        output = JSON_output(message=f'activity_id: {activity_id} from contact_id: {contact_id} belong to user_id: {g.user["id"]} deleted!',
                            g=g, cur=cur)

        return make_response(output, 200)
    else:
        return make_response(jsonify(f'activity id {activity_id} was not found in the database'), 404)
