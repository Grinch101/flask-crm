from flask import Flask, render_template, request, flash, redirect, url_for, make_response, g, session
from models.contact import Contact
from models.user import User
from utility.decor import login_required, path_set
from utility.helpers import conn_pool
from psycopg2.extras import DictCursor

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


@app.after_request
def close_conn(response):
    conn = g.conn
    cur = g.cur
    conn.commit()
    cur.close()
    global connections
    connections.putconn(conn)
    del g.cur
    del g.conn
    return response

############## initiate models ############
phonebook = Contact()
users_handler = User()

############## View Function ##############
@app.route('/', methods=["GET"])
@login_required
def index():
    userid = int(request.cookies.get('user_id'))
    entry = users_handler.find_val(userid)
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
    entry = users_handler.find_val(userid)
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


@app.route('/table', methods=["POST"])
@login_required
def delete():

    uid = int(request.form.get("DELETE"))
    phonebook.delete(uid)
    flash(f"ID:{id} Deleted")

    return redirect(url_for('table'))

# @app.route('/comment', methods=['POST'])
# @sql_pooling
# @login_required
# def comment():
#     uid = int(request.form.get("COMMENT"))
#     row = phonebook.find_row(uid)
#     contact_name = row['contact_name']
#     userid = request.cookies.get('user_id')
#     userid = int(userid)
#     entry = users_handler.find_val(userid)
#     client_name = entry['client_name']

#     session['contact_name'] = contact_name
#     session['userid'] = userid
#     session['row_id'] = uid

#     return render_template('comment.html' , contact_name = contact_name , client_name = client_name)
    

# @app.route('/save_commnet', methods=['POST'])
# @sql_pooling
# @login_required
# def save_comment():

#     text = request.form.get('comment')
#     date = request.form.get('date')

#     contact_name = session['contact_name']
#     row_id = session['row_id']

#     phonebook.leave_comment(text , date, row_id , contact_name)

#     return redirect(url_for('table'))

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
