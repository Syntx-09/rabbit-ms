from flask import Blueprint, render_template, request, flash, jsonify, request, session
from flask_login import login_required, current_user
from .models import Rabbit, Category
from . import db
from datetime import datetime
# from reloading import reloading
from .functions import gen_uid

views = Blueprint('views', __name__)


@views.route('/')
# @login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/list')
@login_required
def list():
    return render_template('rabbit/rabbit_list.html', user=current_user)


@views.route('/list/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        add_category = request.form.get('addCategory')

        new_category = Category(category=add_category)
        db.session.add(new_category)
        db.session.commit()

        flash("Category added successfully", category="success")

    categories = Category.query.filter_by(user_id=current_user.id).all()
    # rabbit = Rabbit.query.
    # categories2 = Rabbit.query.filter(category).all()
    return render_template('rabbit/categories.html', user=current_user, categories=categories, )


@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        category = request.form.get('category')
        if request.form.get('kindled_date') == '':
            kindled_date = datetime.strptime('0001-01-01', '%Y-%m-%d')
        else:
            kindled_date = datetime.strptime(request.form.get('kindled_date'), '%Y-%m-%d')
        uid = gen_uid(6)

        rabbit_name = Rabbit.query.filter_by(name=name).first()
        if rabbit_name:
            flash('A rabbit with that ID already exist', category='error')
        elif len(name) < 2:
            flash('ID must be more than 1 character', category='error')
        else:
            new_rabbit = Rabbit(name=name, sex=sex, category=category, kindled_date=kindled_date, uid=uid,
                                user_id=current_user.id)
            db.session.add(new_rabbit)
            db.session.commit()

            flash('Rabbit added to hutch successfully', category='success')

    return render_template('add.html', user=current_user)


@views.route('/user/overview')
@login_required
def profile():
    # tot = print(Rabbit.query.count())
    rabbit = Rabbit.query.filter_by()
    boy = 'thi id  a s'
    # r1 = dict(Rabbit(name='',sex='',uid='',category='',user_id='', kindled_date=''))
    # r2 = current_user.rabbits
    return render_template('user/user_profile.html', rabbit=[rabbit, boy], user=current_user)


@views.route('/rabbit/<rabbit_id>')
@login_required
def get_rabbit(rabbit_id):
    rabbit = Rabbit.query.filter_by(rab_uid=rabbit_id).first_or_404()
    return render_template('rabbit/rabbit_profile.html', rabbit=rabbit, user=current_user)
