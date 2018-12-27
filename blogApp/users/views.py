from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import current_user, login_user, login_required, logout_user
from blogApp import db
from blogApp.models import User, Post
from blogApp.users.forms import RegistrationForm, LoginForm, UpdateUserForm

users = Blueprint('users', __name__)


#Register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    position=form.position.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

#Login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Use the email given in the form to get the user from the User table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the password is right
        if user.check_password(form.password.data) and user is not None:
            login_user(user)

            # 'next' is saved as the page to be visited after login
            next = request.args.get('next')
            #If 'next' exists go to next, else go to index.html
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html', form=form)




#Logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))
