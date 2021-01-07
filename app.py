from flask import Flask, render_template, request, flash, redirect, url_for
from contact import Contact
import names
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

## View Function ##############

#  injecting some functions to Jinja2 
@app.context_processor
def inject_func():
    return dict(enumerate=enumerate,
                list = list,
                range = range,
                len = len)



phonebook = Contact()
@app.route('/', methods=['POST', "GET"])
def index():

    return render_template('index.html')


@app.route('/saved' , methods=["POST"])
def saved():
    
    input_name = request.form['Name']
    input_number = request.form['Number']
    username = request.form['client_name']
    phonebook.insert(username,input_name,input_number)

    flash(f'{input_number} for {input_name} has been saved')

    return redirect(url_for('index'))


@app.route('/table' , methods=["GET","POST"])
def table():
    
    return render_template('list.html' , mylist = phonebook.db[:10] )


@app.route('/delete' , methods=["GET","POST"])
def delete(): 

    index = int(request.form.get("DELETE"))
    phonebook.delete(index)

    return redirect(url_for('table'))
  



i = 0
while i <= 15000:

    user_length = random.randint(1,5)
    for j in range(user_length):
        client_name = names.get_first_name()
        book_length = random.randint(1,10)
        for k in range(book_length):
            name = names.get_full_name()
            phone = int(random.random()*10000000000)
            phonebook.insert(client_name,name,phone)
            i += 1


if __name__ == "__main__":
    app.run(debug=True)