from flask import request, redirect, url_for, g, flash
from functools import wraps

####### Define Decorator #########



def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if g.user is not None:
            
            return func(*args, **kwargs)
        else:
            flash("Please Login first!")
            return redirect(url_for(('login_form')))
    return wrap
