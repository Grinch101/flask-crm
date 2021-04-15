from flask import request, make_response, g, Blueprint, jsonify
from src.models.user import User
from utility.decor import login_required
from utility.helpers import JSON_output
import jwt
import datetime

user = Blueprint('user', __name__)

users_handler = User()


@user.route('/login', methods=["POST"])
def login():
    secret_key = g.secret_key
    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email, password):
        user_id = users_handler.get_by_email(email)['id']
        token = jwt.encode( payload= {'user_id':user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1) } ,
                            key = secret_key, algorithm="HS256")
                            
        output = JSON_output(message='Logged in', token = token)
        response = make_response(output , 200 )
        response.headers['JWT'] = token

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
        cur = users_handler.add(client_name, email, password)
        output = JSON_output(message='user created!', g=None, cur=cur)

        return make_response(output , 201 )
    else:
        return make_response( jsonify("Signup failed, email's already in use ") , 400)


@user.route('/logout', methods=['PUT'])
@login_required
def logout():
    
    user_id = g.user['id']
    output = JSON_output(message='Logged out!',g=g, cur=None)
    wrong_token = jwt.encode( payload= {'user_id':user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1) } ,
                            key = 'wrong_secret_key', algorithm="HS256")
    # I should drop this, it's here just for fun!                        
    response = make_response(output, 200) 
    response.headers['JWT'] = wrong_token
    return response


