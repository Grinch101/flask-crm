from flask import request, redirect, url_for, g
from utility.helpers import query
from functools import wraps


####### Define Decorator #########


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if request.cookies.get('user_id'):
            return func(*args, **kwargs)
        else:

            return redirect(url_for(('login_form')))
    return wrap
