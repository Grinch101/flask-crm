from flask import request, make_response, g, Blueprint, jsonify
from src.models.user import User
from utility.decor import login_required


user = Blueprint('user', __name__)

users_handler = User()


@user.route('/login', methods=["POST"])
def login():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email, password):
        user_id = users_handler.get_by_email(email)['id']
        response = make_response(jsonify('Successful Login') , 200 )
        response.set_cookie('user_id', str(user_id))
        return response

    else:
        return make_response(jsonify('Email and password are mismatched! please retry!'), 400)


@user.route('/signup', methods=["POST"])
def signup():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")
    client_name = request.form.get("client_name")
    q_email = users_handler.get_by_email(email)
    if q_email is None or q_email['email'] != email:

        users_handler.add(client_name, email, password)
        user_id = users_handler.get_by_email(email)['id']

        response =  make_response( jsonify('user created!', f'ID is {user_id}') , 201 )
        response.set_cookie('user_id', str(user_id))
        return response
    else:

        return make_response( jsonify("Signup failed, email's already in use ") , 400)


@user.route('/logout', methods=['DELETE'])
@login_required
def logout():

    response = make_response(jsonify('cookie deleted'), 200)
    response.set_cookie('user_id', "", max_age=0)
    return response


