from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager

db = SQLAlchemy()
db_name = "user.db"


def myApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bhyre0hnruv'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

   
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Rabbit

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    '''with app.app_context():
        db.create_all()'''

    create_db(app)

    return app

def create_db(app):
    if not path.exists('hutch/' + db_name):
        with app.app_context():
            db.create_all()
        print('Database created!')
