from . import db
from flask_login import UserMixin
from datetime import datetime
from .functions import *


class Rabbit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rab_uid = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(10), unique=True)
    sex = db.Column(db.String(10))
    category = db.Column(db.String(20))
    kindled_date = db.Column(db.DateTime, nullable=True)

    registered_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, name, sex, category, kindled_date, uid, user_id):
        self.name = name
        self.sex = sex
        self.category = category
        self.kindled_date = kindled_date
        self.rab_uid = uid
        self.user_id = user_id

    def __iter__(self):
        iters = dict((key, value) for key, value in Rabbit.__dict__.items() if key[:2] != '__')
        iters.update(self.__dict__)
        for key, value in iters.items():
            yield key, value
        

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(20))
    rabbits = db.relationship('Rabbit', backref='owner', lazy=True)

    def __iter__(self):
        iters = dict((key, value) for key, value in Rabbit.__dict__.items() if key[:2] != '__')
        iters.update(self.__dict__)
        for key, value in iters.items():
            yield key, value

