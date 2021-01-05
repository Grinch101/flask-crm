from flask import Flask, render_template, request
from contact import Contact

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

## View Function ##############
phonbook = Contact()
@app.route('/',methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/saved', methods=["POST"])
def saved():

    username = request.form['client_name']
    input_name = request.form['Name']
    input_number = request.form['Number']

    
    phonbook.insert(username,input_name , input_number)


    return render_template('index.html' , mylist=phonbook.GetAll(), username = username  )


