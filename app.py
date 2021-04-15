from flask import request, g, make_response, jsonify
from src.models.user import User
from src.factory import creat_app
from src.config import DevelopmentConfig, ProductionConfig
from utility.decor import login_required
from utility.helpers import conn_pool
from psycopg2 import DatabaseError, DataError
from jwt import DecodeError
import jwt


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
@app.before_first_request
@app.before_request
def get_secret_key():
    global app
    secret_key = app.config['SECRET_KEY']
    g.secret_key = secret_key

@app.before_request
def open_conn():
    global connections
    g.conn = connections.getconn()

@app.before_request
def user_auth():
    if request.headers.get('JWT'):
        token = request.headers['JWT']
        secret_key = g.secret_key
        try:
            data = jwt.decode(token, key = secret_key ,algorithms=["HS256"])
            user_id = int(data['user_id'])
            g.user =  users_handler.get_by_id(user_id)

        except DecodeError as e:
            return jsonify(f'Token invalid,  {e}')
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

    return make_response(jsonify("Database Error!") , 500 )


if __name__ == "__main__":
    app.run()
