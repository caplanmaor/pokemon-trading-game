from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from app.forms import LogInForm, SignUpForm
from app import db
from app.models import Users

users_bp = Blueprint('users_bp',__name__,
    template_folder='templates',
    static_folder='static', 
    static_url_path='assets')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_formi = LogInForm()
    if login_formi.validate_on_submit():
        logout_user()
        username = login_formi.username.data
        password = login_formi.password.data
        user = Users.query.filter_by(name=username).first()        
        # check password
        if not user or not check_password_hash(user.password, password):
            return 'wrong password or username doesnt exist'
        # log in
        login_user(user, remember=True)
        return redirect(url_for('profiles_bp.display'))
    return render_template('login.html', form=login_formi)

@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_formi = SignUpForm()
    if signup_formi.validate_on_submit():
        username = signup_formi.username.data
        email = signup_formi.email.data
        password1 = signup_formi.password1.data
        password2 = signup_formi.password2.data

        # check if already exists
        temp_user = Users.query.filter_by(email=email).first()
        if temp_user:
            return "a user already exists with this email"

        if password1 != password2:
            return "passwords dont match"

        # create user
        user = Users(email=email, name=username, password=generate_password_hash(password1, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users_bp.login'))
    return render_template('signup.html', form=signup_formi)

@users_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('users_bp.login'))