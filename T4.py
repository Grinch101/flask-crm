from flask import Flask, render_template, request, flash, redirect, url_for, make_response, g
from models.contact import Contact
from models.user import User
from utility.decor import sql_connection, login_required, path_set


app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'


@app.route('/' , methods=['GET'])
def index():
    return render_template('test.html')


@app.route('/' , methods=['POST'])
def home_page():

    email = request.form.get("inputEmail")
    g.email = email
    return redirect(url_for('welcome'))

@app.route('/index')
def welcome():
    val = g.email
    return render_template(f'<h1> hello {val} </h1>')


if __name__=='__main__':
    app.run(debug= True)
