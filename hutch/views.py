from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user 
from .models import Rabbit
from . import db

views = Blueprint('views', __name__)

@views.route('/')
#@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/list')
@login_required
def list():
    return render_template('list.html', user=current_user)

@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        category = request.form.get('category')

        rabbit_name = Rabbit.query.filter_by(name=name).first()
        if rabbit_name:
            flash('A rabbit with that ID already exist', category='error')
        elif len(name) < 2:
            flash('ID must be more than 1 character', category='error')
        else:
            new_rabbit= Rabbit(name=name, sex=sex, category=category, user_id=current_user.id)
            db.session.add(new_rabbit)
            db.session.commit()

            flash('Rabbit added to hutch successfully', category = 'success')
            
    return render_template('add.html', user=current_user)

@views.route('/user')
@login_required
def profile():
    #tot = print(Rabbit.query.count())
    return render_template('profile.html', user = current_user)

@views.route('/details/')
@login_required
def rab_profile(id=2):

    rabbit = Rabbit.query.filter_by(id=2).first()
    # if rabbit:
    #     return jsonify({
    #         'id': rabbit.name,
    #         'sex': rabbit.sex
    #     })
    # # name = Rabbit.name
    return render_template('rabbit/rabbit_profile.html', rabbit=rabbit, user=current_user)