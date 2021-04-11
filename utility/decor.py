from flask import  g, make_response, jsonify
from functools import wraps

####### Define Decorator #########



def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if g.user is not None:
            
            return func(*args, **kwargs)
        else:

            return make_response(jsonify('Please login!'), 401)
    return wrap
