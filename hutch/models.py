from . import db
from flask_login import UserMixin


class Rabbit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    sex = db.Column(db.String(10))
    category = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, sex, category, user_id):
        self.name = name
        self.sex = sex
        self.category = category
        self.user_id = user_id
        

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(20))
    rabbits = db.relationship('Rabbit', backref='owner', lazy=True)
