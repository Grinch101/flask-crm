from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, make_response, g
from models.user import User
from utility.decor import login_required

user = Blueprint('user', __name__)

users_handler = User()


@user.route('/login', methods=["GET"])
def login_form():

    return render_template('login.html')


@user.route('/login_check', methods=["POST"])
def login_check():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")

    if users_handler.validate(email, password):
        user_id = users_handler.get_by_email(email)['id']
        response = make_response(redirect(url_for('contact.index')))
        response.set_cookie('user_id', str(user_id))
        return response

    else:

        flash('Wrong Email or Password. Please try again, or Sign-up!')
        return redirect(url_for('user.login_form'))


@user.route('/signup', methods=["GET"])
def signup_form():

    return render_template('signup.html')


@user.route('/signup', methods=["POST"])
def signup():

    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")
    client_name = request.form.get("client_name")
    q_email = users_handler.get_by_email(email)
    if q_email is None or q_email['email'] != email:

        users_handler.add(client_name, email, password)
        user_id = users_handler.get_by_email(email)['id']

        response = make_response(redirect(url_for('contact.index')))
        response.set_cookie('user_id', str(user_id))
        return response
    else:
        flash('Email in use, please login')
        return redirect(url_for('user.signup_form'))


@user.route('/logout', methods=['POST'])
@login_required
def logout():

    response = make_response(redirect(url_for('user.login_form')))
    response.set_cookie('user_id', "", max_age=0)
    return response
