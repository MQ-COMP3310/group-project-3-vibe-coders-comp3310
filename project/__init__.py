from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  

#Task 7 - sets login view to prevent unauthorized access
login_manager.login_view = 'main.login'

#user loader for session management
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    #parameterized query
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-do-not-reveal'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Now this will work

    # Register blueprints
    from .json import json as json_blueprint
    app.register_blueprint(json_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app