from flask import Flask, render_template, request, flash, redirect, url_for
from contact import Contact

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

## View Function ##############

#  injecting some functions to Jinja2 
@app.context_processor
def inject_enumerate():
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
    
    show_list = phonebook.GetAll()
 
    return render_template('list.html' , mylist = show_list)

@app.route('/delete' , methods=["GET","POST"])
def delete(): 

    db = phonebook.GetAll() 

    index = request.form.get("DELETE")
    index = int(index)
    val = db[index]
    phonebook.delete(val)
    return redirect(url_for('table'))
  

if __name__ == "__main__":
    app.run(debug=True)