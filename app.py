from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from models.contact import Contact
from models.user import User
from utility.decor import sql_connection, login_required, path_set


app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

#  injecting some functions to Jinja


@app.context_processor
def inject_func():
    return dict(enumerate=enumerate,
                list=list,
                range=range,
                len=len)


## initiate ###################
phonebook = Contact()
users_handler = User()

## View Function ##############


@app.route('/', methods=["GET"])
@sql_connection
@login_required
def index(cur, conn):
    userid = int(request.cookies.get('user_id'))
    entry = users_handler.find_val(userid, cur, conn)
    username = entry['client_name']
    return render_template('index.html', username=username)


@app.route('/login', methods=["GET"])
def login_form():
    flash("Please Login first!")
    return render_template('login.html')


@app.route('/login_check', methods=["POST"])
@sql_connection
def login_check(cur, conn):

    # cur = kwargs['cur']
    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email, password, cur, conn):

        userid = users_handler.find_userid_by_email(email, cur, conn)
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
@sql_connection
def signup(cur, conn):

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")
    client_name = request.form.get("client_name")

    if not users_handler.old_user(email, cur, conn):

        users_handler.add( client_name, email, password, cur, conn)
        userid = users_handler.find_userid_by_email(email, cur, conn)

        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id', str(userid))
        return response
    else:
        flash('Email in use, please login')
        return redirect(url_for('signup_form'))


@app.route('/saved', methods=["POST"])
@sql_connection
@login_required
def saved(cur, conn):

    input_name = request.form['Name']
    input_number = request.form['Number']
    userid = request.cookies.get('user_id')
    userid = int(userid)
    entry = users_handler.find_val(userid, cur, conn)
    client_name = entry['client_name']

    # value = {   'userid'        :userid,
    #             # 'client_name'   :client_name,
    #             'name'          :input_name ,
    #             'phone'         :input_number}

    phonebook.add(userid, input_name, input_number, cur, conn)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('index'))


@app.route('/table', methods=["GET"])
@sql_connection
@login_required
def table(cur, conn):

    userid = request.cookies.get('user_id')
    userid = int(userid)
    contact_list = phonebook.find_book(userid, cur, conn)

    return render_template('list.html', mylist=contact_list)


@app.route('/delete', methods=["POST"])
@sql_connection
@login_required
def delete(cur, conn):

    id = int(request.form.get("DELETE"))
    phonebook.delete(id, cur, conn)
    flash(f"ID:{id} Deleted")

    return redirect(url_for('table'))


@app.route('/logout', methods=['POST'])
@login_required
def logout():

    response = make_response(redirect(url_for('login_form')))
    response.set_cookie('user_id', "", max_age=0)
    return response


@app.route('/behind-the-scene', methods=['GET'])
@sql_connection
def behind(cur, conn):

    if request.cookies.get('user_id'):
        list1 = phonebook.get_all(cur, conn)
        userid = request.cookies.get('user_id')
        userid = int(userid)
        list2 = phonebook.find_book(userid, cur, conn)
        list3 = users_handler.list
        dic1 = phonebook.id_index
        # dic2 = users_handler.email_userid

        return render_template('behind-the-scene.html', dic1=dic1,
                               dic2=dic2,
                               list1=list1,
                               list2=list2,
                               list3=list3)

    else:
        return render_template('behind-the-scene.html')

# import names
# import random
# i = 0
# while i <= 150:

#     user_length = random.randint(1,5)
#     for j in range(user_length):
#         client_name = names.get_first_name()
#         book_length = random.randint(1,10)
#         for k in range(book_length):
#             name = names.get_full_name()
#             phone = int(random.random()*10000000000)
#             phonebook.insert(client_name,name,phone)
#             i += 1


if __name__ == "__main__":
    app.run(debug=True)
