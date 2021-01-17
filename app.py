from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from models.contact import Contact
from models.user import User
import names
import random
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

#########################
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if request.cookies.get('user_id'):
            return func(*args, **kwargs)
        else:
            
            return redirect(url_for(('login_form')))
    return wrap

#  injecting some functions to Jinja2 
@app.context_processor
def inject_func():
    return dict(enumerate=enumerate,
                list = list,
                range = range,
                len = len)


## initiate ###################
phonebook = Contact()
users_handler = User()

## View Function ##############

@app.route('/', methods=["GET"])
@login_required
def index():
    userid = int(request.cookies.get('user_id'))
    entry = users_handler.find_val(userid)
    username = entry['client_name']
    return render_template('index.html' , username = username)
 


@app.route('/login' , methods=["GET"])
def login_form():
    flash("Please Login first!")
    return render_template('login.html')


@app.route('/login_check', methods=["POST"])
def login_check():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email , password):

        userid = users_handler.find_userid_by_email(email)
        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id' , str(userid))    
        return response

    else:
    
        flash('Wrong Email or Password. Please try again, or Sign-up!')
        return redirect(url_for('login_form'))
    

@app.route('/signup', methods=["GET"] )
def signup_form():

    return render_template('signup.html')


@app.route('/signup', methods=["POST"] )
def signup():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")
    client_name = request.form.get("client_name")
    entry = {   'client_name':client_name,
                'email':email,
                'password':password}

    if not users_handler.old_user(email):

        users_handler.register(entry)
        userid = users_handler.email_userid[email]

        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id' , str(userid)) 
        return response
    else:
        flash('Email in use, please login')
        return redirect(url_for('signup_form'))



@app.route('/saved' , methods=["POST"])
@login_required
def saved():
    
    input_name = request.form['Name']
    input_number = request.form['Number']
    userid = request.cookies.get('user_id')
    userid = int(userid)
    entry = users_handler.find_val(userid)
    username = entry.get('client_name')

    entry = {   'userid'        :userid,	        
                'client_name'   :username,
                'name'          :input_name,
                'phone'         :input_number}

    phonebook.insert(entry)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('index'))


@app.route('/table' , methods=["GET"])
@login_required
def table():
    
    userid = request.cookies.get('user_id')
    userid = int(userid)
    contact_list = phonebook.find_book(userid)

    return render_template('list.html' , mylist = contact_list )



@app.route('/delete' , methods=["POST"])
@login_required
def delete(): 

    id = int(request.form.get("DELETE"))
    phonebook.delete(id)
    flash(f"ID:{id} Deleted")

    return redirect(url_for('table'))
  
@app.route('/logout' , methods=['POST'])
@login_required
def logout():
    
    response = make_response(redirect(url_for('login_form')))
    response.set_cookie('user_id' , "" , max_age = 0)
    return response


@app.route('/behind-the-scene', methods=['GET'])
def behind():

    if request.cookies.get('user_id'):
        list1 = phonebook.GetAll()
        userid = request.cookies.get('user_id')
        userid = int(userid)
        list2 = phonebook.find_book(userid)
        list3 = users_handler.users_list

        dic1 = phonebook.id_index_dict
        # dic2 = phonebook.id_userid

        # dic3 = users_handler.userid_password
        # dic4 = users_handler.userid_username
        dic2 = users_handler.email_userid

        return render_template('behind-the-scene.html', dic1=dic1,
                                                        dic2=dic2,
                                                        list1=list1,
                                                        list2 = list2,
                                                        list3=list3)
    
    else :
        return render_template('behind-the-scene.html' )


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