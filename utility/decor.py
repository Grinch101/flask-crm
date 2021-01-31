from flask import request, redirect, url_for
from utility.helpers import connection_closer , connection_opener, query
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


################################
def sql_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cur , conn = connection_opener()
        
        kwargs['cur'] = cur
        kwargs['conn'] = conn
        output = func(  *args, **kwargs )
        connection_closer(cur , conn)
        if output:
            return output
    
    return wrapper


## another love making with decorator concept! :) 
def path_set( path ):
    def query_decorator(func):
        def wrapper(*args, **kwargs):

            kwargs['path'] = path
            return func(  *args, **kwargs)
        return wrapper
    return query_decorator
