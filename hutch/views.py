from flask import Blueprint, render_template, request, flash, jsonify, request, session
from flask_login import login_required, current_user
from .models import Rabbit, Category
from . import db
from datetime import datetime
from .functions import gen_uid

views = Blueprint('views', __name__)


@views.route('/')
# @login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('rabbit/list')
@login_required
def list():
    #list all rabbits owned by user
    return render_template('rabbit/rabbit_list.html', user=current_user)


@views.route('/rabbit/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        add_category = request.form.get('addCategory')

        new_category = Category(category=add_category, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()

        flash("Category added successfully", category="success")
    rabbit = Rabbit.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('rabbit/categories.html', user=current_user, categories=categories, rabbit=rabbit)


@views.route('/addRabbit', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        category = request.form.get('category')
        if request.form.get('kindled_date') == '':
            kindled_date = datetime.strptime('1101-01-01', '%Y-%m-%d')
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
    category = Category.query.filter_by(user_id = current_user.id)

    return render_template('rabbit/addRabbit.html', user=current_user, category = category)


@views.route('/user/overview')
@login_required
def user_profile():
    rabbit = Rabbit.query.filter_by()
    boy = 'thi id  a s'
    return render_template('user/user_profile.html', rabbit=[rabbit, boy], user=current_user)


@views.route('/rabbit/<rabbit_uid>', methods=['GET', 'POST'])
@login_required
def get_rabbit(rabbit_uid):
    #retrieve rabbit profile
    category = Category.query.filter_by(user_id = current_user.id)
    rabbit = Rabbit.query.filter_by(rab_uid=rabbit_uid).first_or_404()

    #Update rabbit details/Profile
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        category = request.form.get('category')
        if request.form.get('kindled_date') == '':
            kindled_date = datetime.strptime('1101-01-01', '%Y-%m-%d')
        else:
            kindled_date = datetime.strptime(request.form.get('kindled_date'), '%Y-%m-%d')
        uid = gen_uid(6)

        rabbit_name = Rabbit.query.filter_by(name=name).first()
        if rabbit_name:
            flash('A rabbit with that ID already exist', category='error')
        elif len(name) < 2:
            flash('ID must be more than 1 character', category='error')
        else:
            rabbit = Rabbit(name=name, sex=sex, category=category, kindled_date=kindled_date, uid=uid,
                                user_id=current_user.id)
            db.session.add(rabbit)
            db.session.commit()


            flash('Rabbit updated successfully', category='success')

    return render_template('rabbit/rabbit_profile.html', category=category, rabbit=rabbit, user=current_user)

@views.route('/rabbit/<rabbit_uid>/')
@login_required
def delete_rabbit(rabbit_uid):
    rabbit = Rabbit.query.filter_by(rab_uid=rabbit_uid).first_or_404()
    db.session.delete(rabbit)
    db.session.commit()
    return render_template('rabbit/rabbit_list.html', user=current_user)
