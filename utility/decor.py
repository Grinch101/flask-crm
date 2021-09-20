import jwt
import json
from flask import  g, jsonify, request
from functools import wraps
from jwt import DecodeError
from src.models.user import User
from utility.helpers import json_output

####### Define Decorator #########
users_handler = User()

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        token = request.headers.get('JWT')
        if token:
            secret_key = g.secret_key
            try:
                data = jwt.decode(token, key=secret_key, algorithms=["HS256"])
                user_id = int(data['user_id'])
                g.user = users_handler.get_by_id(user_id)
                return func(*args, **kwargs)
            except DecodeError as e:
                return json_output(error='Token invalid,  {e}', http_code= 403) # forbidden!
        else:
            g.user = None
            return json_output(error= 'Please login!', http_code= 401) # unauthorized!
    return wrap

