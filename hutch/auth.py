from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user 


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
    	return redirect(url_for('views.home'))
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login Success', category ='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Password', category='error')
        else:
            flash('Username does not exist.', category='error')
   
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
    	return redirect(url_for('views.home'))
    if request.method == 'POST':
        username = request.form.get('username').lower()
        email = request.form.get('email').lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(email) < 5:
            flash('Email is not valid', category='error')
        elif len(username) < 3:
            flash('Username must exceed 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords didn\'t match', category='error')
        elif len(password1) <4:
            flash('Password must exceed 3 characters')
        else:
            new_user = User(username= username, email=email, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            #login_user(user, remember=True)
            flash('Account created!', category = 'success')
            return redirect(url_for('auth.login'))

        
    return render_template('signup.html', user=current_user)