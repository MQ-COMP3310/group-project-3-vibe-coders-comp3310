from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import flask-login
from flask_login import LoginManager
from flask_migrate import Migrate, migrate

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
#task 7 setting up flask login
"""'''
# init flask-login
login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    #this is the function that loads the user
    #it takes the user id and returns the user object
    #this is used by flask-login to load the user
    return User.query.get(int(user_id))
"""

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-do-not-reveal'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
  
    #login_manager.init_app(app)

    #import user after init db
    #from .models import User

    # blueprint for auth routes in our app
    from .json import json as json_blueprint
    app.register_blueprint(json_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
