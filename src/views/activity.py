
import json
from flask import Blueprint, request, g
from src.models.activity import Activity
from src.models.contact import Contact
from utility.decor import login_required
from utility.helpers import json_output


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
        data = cur.fetchall()
        if data is not None and data != []:
            return json_output(
                message=f'All activity retrived',
                data=data, http_code=200
                )
        else:
            return json_output(error='No activity found!', http_code=404)
    else:
        return json_output(error='Contact not found!', http_code=404)


@activity.route('/<int:contact_id>', methods=["POST"])
@login_required
def add(contact_id):
    action = request.josn['action']
    description = request.json['description']
    date = request.json['date']
    time = request.json['time']
    if all([action, date, time]):
        cur = activities.add(action, description, date, time,
                             g.user['id'], contact_id)
        if cur:
            data = cur.fetchone()
            return json_output(message='Activity Added!',
                               data=data, http_code=201)
        else:
            return json_output(error='contact was not found!', http_code=404)
    else:
        return json_output(error='incomplete request!', http_code=401)


@activity.route('/<int:contact_id>/delete/<int:activity_id>',
                methods=["DELETE"])
@login_required
def delete(contact_id, activity_id):
    if all([contact_id, activity_id]):
        cur = activities.delete(contact_id, activity_id)
        if cur:
            data = cur.fetchone()
            return json_output(
                message=f'''activity_id: {activity_id} from
                contact_id: {contact_id}
                belong to user_id: {g.user["id"]} deleted!''',
                data=data, http_code=200)
        else:
            if not cur[0] and cur[1] == 'activity was not found!':
                return json_output(
                    message=f'''activity id {activity_id}
                    was not found in the database''',
                    http_code=404)
            elif not cur[0] and cur[1] == 'contact was not found!':
                return json_output(error='incomplete request!', http_code=400)
