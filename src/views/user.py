import json
import datetime
import jwt
from jwt import DecodeError
from flask import request,  g, Blueprint
from src.models.user import User
from utility.decor import login_required
from utility.helpers import json_output, secure_g


user = Blueprint('user', __name__)
users_handler = User()


@user.route('/login', methods=["POST"])
def login():
    secret_key = g.secret_key
    email = request.json["inputEmail"]
    password = request.json["inputPassword"]

    if users_handler.validate(email, password):
        user_id = users_handler.get_by_email(email).fetchone()['id']
        token = jwt.encode(
            payload={'user_id': user_id,
                     'exp': datetime.datetime.utcnow()
                     + datetime.timedelta(days=10)
                     },
            key=secret_key,
            algorithm="HS256"
        )
        return json_output(message='Logged in, token generated', data=token)
    else:
        if users_handler.get_by_email(email):
            return json_output(
                error='Wrong Email or Password! please retry!',
                http_code=400
            )
        else:
            return json_output(error='email not found, please sign up',
                               http_code=404
                               )


@user.route('/signup', methods=["POST"])
def signup():
    email = request.json["inputEmail"]
    password = request.json["inputPassword"]
    client_name = request.json["client_name"]

    if not users_handler.get_by_email(email):
        cur = users_handler.add(client_name, email, password)
        data = cur.fetchone()
        return json_output(message='user created!', data=data, http_code=201)
    else:
        return json_output(error='signup failed, email in use!', http_code=400)

# This route will be drop in the next commit


@user.route('/logout', methods=['PUT'])
@login_required
def logout():
    user_id = g.user['id']
    output = json_output(message='Logged out!')
    wrong_token = jwt.encode(
        payload={'user_id': user_id,
                 'exp': datetime.datetime.utcnow()
                 + datetime.timedelta(days=1)},
        key='wrong_secret_key',
        algorithm="HS256")
    # I should drop this, it's here just for fun!
    output.headers['JWT'] = wrong_token
    return output


@user.route('/current_user', methods=['GET'])
@login_required
def current_user():
    return json_output(message='user info', data=secure_g(g))


@user.route('/user_update', methods=['PUT'])
@login_required
def user_update():

    if request.json:
        column_list = list(request.json.keys())
        new_email = request.json.get('new_email')
        new_password = request.json.get('new_password')
        new_name = request.json.get('new_name')
        all_input_list = [new_email, new_name, new_password]
        user_id = g.user['id']
        current_info = users_handler.get_by_id(user_id)
        current_info = dict(current_info)
        for item in column_list:
            current_info[item] = request.form.get(item)

        cur = users_handler.update(
                        user_id,
                        current_info['email'],
                        current_info['client_name'],
                        current_info['passkey'])
                        
        data = dict(cur.fetchone())
        data.pop('passkey')
        data = {**data, 'updated columns': column_list}
        return json_output(message='updated', data=data)

    else:
        return json_output(error='incomplete request!', http_code=400)
