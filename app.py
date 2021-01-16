from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from MyModels.contact import Contact
from MyModels.user import User
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



phonebook = Contact()

## View Function ##############

@app.route('/', methods=['POST', "GET"])
def index():
    if request.cookies.get('email'):

        return render_template('index.html')
    else:
        return render_template('login.html')



@app.route('/logged_in', methods=['GET',"POST"])
def logged_in():

    users_handler = User()
   
    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email , password):

        return redirect(url_for('index'))

    else:
        users_handler.register(email,password)

        response = make_response(render_template('index.html'))
        response.set_cookie('email',email)

        return response

@app.route('/saved' , methods=["POST"])
def saved():
    
    input_name = request.form['Name']
    input_number = request.form['Number']
    username = request.cookies.get('email')
    phonebook.insert(username,input_name,input_number)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('index'))


@app.route('/table' , methods=["GET","POST"])
def table():
    
    username = request.cookies.get('email')

    contact_list = [ i for i in phonebook.db if i.get('client_name')==username ]

    return render_template('list.html' , mylist = contact_list )


@app.route('/delete' , methods=["GET","POST"])
def delete(): 

    id = int(request.form.get("DELETE"))
    phonebook.delete(id)
    flash(f"ID:{id} Deleted")

    return redirect(url_for('table'))
  



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