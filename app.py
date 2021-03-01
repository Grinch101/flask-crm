from flask import render_template, request, g, redirect, url_for
from models.user import User
from src.factory import creat_app
from src.config import DevelopmentConfig, ProductionConfig
from utility.decor import login_required
from utility.helpers import conn_pool
from psycopg2 import DatabaseError, DataError


# create app and register blueprints
app = creat_app(DevelopmentConfig)

# Create a Global Connetion Pool:
connections = conn_pool(1, 10)


############## initiate models ############
users_handler = User()

#  injecting some functions to Jinja


@app.context_processor
def inject_func():
    return dict(enumerate=enumerate,
                list=list,
                range=range,
                len=len,
                int=int)


###### before and after each request ########
@app.before_request
def open_conn():
    global connections
    g.conn = connections.getconn()


@app.before_request
def user_ident():
    if request.cookies.get('user_id'):
        user_id = int(request.cookies.get('user_id'))
        g.user = users_handler.get_by_id(user_id)
    else:
        g.user = None


@app.after_request
def close_conn(response):
    if g.conn is not None:
        g.conn.commit()
        g.conn.cursor().close()
        global connections
        connections.putconn(g.conn)
        return response
    else:
        return response


########### Error handler ###########

@app.errorhandler(DataError)
@app.errorhandler(DatabaseError)
def rollback_changes(error):
    g.conn.cursor().close()
    g.conn.rollback()
    global connections
    connections.putconn(g.conn)
    g.conn = None

    return render_template('error.html', error=error)


@app.route('/')
@login_required
def index():

    return redirect('/contact-management/')


if __name__ == "__main__":
    app.run()
