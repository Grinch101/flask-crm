from flask import request, redirect, url_for, g
from utility.helpers import query
from functools import wraps
from models.user import User
####### Define Decorator #########
users_handler = User()


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if g.user_id is not None:
            
            return func(*args, **kwargs)
        else:
            return redirect(url_for(('login_form')))
    return wrap
