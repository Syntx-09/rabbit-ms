from flask import Blueprint, render_template, request, flash, jsonify , request, session
from flask_login import login_required, current_user 
from .models import Rabbit
from . import db
from datetime import datetime
#from reloading import reloading
from .functions import gen_uid

views = Blueprint('views', __name__)

@views.route('/')
#@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/list')
@login_required
def list():
    return render_template('rabbit/rabbit_list.html', user=current_user)

@views.route('/list/categories')
def categories():

    return render_template('rabbit/categories.html', user=current_user)

@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        category = request.form.get('category')
        kindled_date = datetime.strptime(request.form.get('kindled_date'), '%Y-%m-%d')
        uid = gen_uid(6)
        

        rabbit_name = Rabbit.query.filter_by(name=name).first()        
        if rabbit_name:
        	flash('A rabbit with that ID already exist', category='error')
        elif len(name) < 2:
        	flash('ID must be more than 1 character', category='error')
        else:
            new_rabbit= Rabbit(name=name, sex=sex, category=category, kindled_date=kindled_date, uid = uid, user_id=current_user.id)
            db.session.add(new_rabbit)
            db.session.commit()


            flash('Rabbit added to hutch successfully', category = 'success')
            
    return render_template('add.html', user=current_user)

@views.route('/user/overview')
@login_required
def profile():
    #tot = print(Rabbit.query.count())
    rabbit = Rabbit.query.filter_by()
    r1 = dict(Rabbit(name='',sex='',category='',user_id='', kindled_date=''))
    r2 = current_user.rabbits
    return render_template('user/user_profile.html', rabbit=rabbit, r1=r1, user = current_user)

@views.route('/rabbit/<rabbit_id>')
@login_required
def get_rabbit(rabbit_id): 
    rabbit = Rabbit.query.filter_by(id = rabbit_id).first_or_404()
    return render_template('rabbit/rabbit_profile.html', rabbit=rabbit, user=current_user)