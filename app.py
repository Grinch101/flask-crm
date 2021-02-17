from flask import Flask, render_template, request, flash, redirect, url_for, make_response, g, session
from models.contact import Contact
from models.user import User
from utility.decor import login_required, path_set
from utility.helpers import conn_pool, query
from psycopg2.extras import DictCursor
from psycopg2 import DatabaseError, DataError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'




### Create a Global Connetion Pool:
connections = conn_pool(1,10)

#  injecting some functions to Jinja
@app.context_processor
def inject_func():
    return dict(enumerate=enumerate,
                list=list,
                range=range,
                len=len)


###### before and after each request ########
@app.before_request
def open_conn():
    global connections
    conn = connections.getconn()
    cursor = conn.cursor(cursor_factory = DictCursor)
    g.cur = cursor
    g.conn = conn
    g.error = False


@app.after_request
def close_conn(response):
    
    if g.conn is not None:    
        conn = g.conn
        cur = g.cur
        conn.commit()
        cur.close()
        global connections
        connections.putconn(conn)
        return response
    else:
        return response


# @app.teardown_request
# def tear(error=None):
#     if g.conn is not None:
#         cur = g.cur
#         conn = g.conn
#         conn.rollback()
#         print('rolled back')
#         cur.close()
#         connections = globals()['connections']
#         connections.putconn(conn)
#         del g.conn

########### Error handler ###########
@app.errorhandler(DataError)
@app.errorhandler(DatabaseError)
def roll_back_changes(error):
    cur = g.cur
    conn = g.conn
    cur.close()
    conn.rollback()
    connections = globals()['connections']
    connections.putconn(conn)
    g.conn = None
    return '<h1> ERROR </h1>'



############## initiate models ############
phonebook = Contact()
users_handler = User()

############## View Function ##############

@app.route('/debug', methods=["GET"])
def debug():
    email = "inputEmail"
    password = "inputPassword"
    client_name = "client_name"
    users_handler.add( client_name, email, password)


    query('SQL/user', 'fake_query', (1,))
    return render_template('comment.html', error='error')



@app.route('/', methods=["GET"])
@login_required
def index():
    userid = int(request.cookies.get('user_id'))
    entry = users_handler.find_val_by_id(userid)
    username = entry['client_name']
    return render_template('index.html', username=username)


@app.route('/login', methods=["GET"])
def login_form():
    flash("Please Login first!")
    return render_template('login.html')


@app.route('/login_check', methods=["POST"])
def login_check():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email, password):

        userid = users_handler.find_userid_by_email(email)
        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id', str(userid))
        return response

    else:

        flash('Wrong Email or Password. Please try again, or Sign-up!')
        return redirect(url_for('login_form'))


@app.route('/signup', methods=["GET"])
def signup_form():

    return render_template('signup.html')


@app.route('/signup', methods=["POST"])
def signup():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")
    client_name = request.form.get("client_name")

    if not users_handler.old_user(email):

        users_handler.add( client_name, email, password)
        userid = users_handler.find_userid_by_email(email)

        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id', str(userid))
        return response
    else:
        flash('Email in use, please login')
        return redirect(url_for('signup_form'))


@app.route('/saved', methods=["POST"])
@login_required
def saved():

    input_name = request.form['Name']
    input_number = request.form['Number']
    userid = request.cookies.get('user_id')
    userid = int(userid)
    entry = users_handler.find_val_by_id(userid)
    client_name = entry['client_name']
    phonebook.add(userid, input_name, input_number)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('index'))


@app.route('/table', methods=["GET"])
@login_required
def table():

    userid = request.cookies.get('user_id')
    userid = int(userid)
    contact_list = phonebook.find_book(userid)

    return render_template('list.html', mylist=contact_list)


@app.route('/delete/contacts/<id>', methods=["POST"])
@login_required
def delete(id):

    phonebook.delete(id)
    flash(f"ID:{id} Deleted")

    return make_response(redirect(url_for('table')))


@app.route('/logout', methods=['POST'])
@login_required
def logout():

    response = make_response(redirect(url_for('login_form')))
    response.set_cookie('user_id', "", max_age=0)
    return response


@app.route('/behind-the-scene', methods=['GET'])
def behind():

    if request.cookies.get('user_id'):
        list1 = phonebook.get_all()
        userid = request.cookies.get('user_id')
        userid = int(userid)
        list2 = phonebook.find_book(userid)
        list3 = users_handler.get_all()


        return render_template('behind-the-scene.html',
                               list1=list1,
                               list2=list2,
                               list3=list3)

    else:
        return render_template('behind-the-scene.html')


if __name__ == "__main__":
    app.run(debug=True)
