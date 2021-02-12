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


############ work with one connection ##############
def sql_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cur, conn = open_conn()

        g.cur = cur
        g.conn = conn
        output = func(*args, **kwargs)
        close_conn(cur, conn)
        if output:
            return output

    return wrapper

############ work with Connection pool ##############


def sql_pooling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        # cur, conn, pool = open_pool(1 ,10)
        g.cur = get_cursor(1,10)
        output = func(*args, **kwargs)
        # put_conn(pool, conn)
        if output:
            return output

    return wrapper


# another love making with decorator concept! :)
def path_set(path):
    def query_decorator(func):
        def wrapper(*args, **kwargs):

            kwargs['path'] = path
            return func(*args, **kwargs)
        return wrapper
    return query_decorator
