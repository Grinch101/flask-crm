from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from contact import Contact
from user import User
import names
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'



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

@app.route('/', methods=["GET",'POST'])
def index():
    if request.cookies.get('user_id'):
        userid = int(request.cookies.get('user_id'))
        username = users_handler.userid_username.get(userid)
        return render_template('index.html' , username = username)
    else:
        return render_template('login.html')



@app.route('/login_check', methods=["POST"])
def login_check():

   
    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email , password):

        userid = users_handler.email_userid[email]
        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id' , str(userid))    
        return response

    else:
    
        flash('Wrong Email or Password. Please try again, or Sign-up!')
        return render_template('login.html')


@app.route('/signup', methods=['GET',"POST"] )
def signup():

    if request.form.get("submit")=='CLICKED':

        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        client_name = request.form.get("client_name")

        if not users_handler.old_user(email):

            users_handler.register(client_name,email,password)
            userid = users_handler.email_userid[email]

            response = make_response(redirect(url_for('index')))
            response.set_cookie('user_id' , str(userid)) 
            return response
    
        else:

            flash('Login Failed!')
            return render_template('signup.html')
    
    else:   

        return render_template('signup.html')
    

@app.route('/saved' , methods=["POST"])
def saved():
    
    input_name = request.form['Name']
    input_number = request.form['Number']
    userid = request.cookies.get('user_id')
    userid = int(userid)
    username = users_handler.userid_username[userid]

    phonebook.insert(userid,username,input_name,input_number)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('index'))


@app.route('/table' , methods=["GET", "POST"])
def table():
    
    if request.cookies.get('user_id'):
        userid = request.cookies.get('user_id')
        userid = int(userid)
        contact_list = phonebook.find_book(userid)

        return render_template('list.html' , mylist = contact_list )
    else:
        return render_template('login.html')


@app.route('/delete' , methods=["POST"])
def delete(): 

    id = int(request.form.get("DELETE"))
    phonebook.delete(id)
    flash(f"ID:{id} Deleted")

    return redirect(url_for('table'))
  
@app.route('/logout' , methods=['GET'])
def logout():
    
    response = make_response(render_template('login.html'))
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
        dic2 = phonebook.id_userid

        dic3 = users_handler.userid_password
        dic4 = users_handler.userid_username
        dic5 = users_handler.email_userid

        return render_template('behind-the-scene.html', dic1=dic1,
                                                        dic2=dic2,
                                                        dic3=dic3,
                                                        dic4=dic4,
                                                        dic5=dic5, 
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