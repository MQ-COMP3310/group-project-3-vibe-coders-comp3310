from . import db
#import werkzeug securtiy to  hash passwords
from werkzeug.security import generate_password_hash, check_password_hash
#help with login
from flask_login import UserMixin

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class MenuItem(db.Model):
    name = db.Column(db.String(80), nullable = False)
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'       : self.name,
           'description' : self.description,
           'id'         : self.id,
           'price'      : self.price,
           'course'     : self.course,
       }
    
#Task 7
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    #task 9 additional feature 1
    security_question = db.Column(db.String(200), nullable=False) 
    security_answer_hash = db.Column(db.String(128), nullable=False)
    
    restaurants = db.relationship('Restaurant', backref='owner', lazy=True)
    
    def set_password(self, password):
        #Uses werkzeug's generate_password_hash
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        #Uses constant-time comparison to prevent timing attacks
        return check_password_hash(self.password_hash, password)
    
    #task 9 additional feature 1
    def set_security_answer(self, answer):
        #security answers are hased like passwords
        self.security_answer_hash = generate_password_hash(answer.lower())  
    
    def check_security_answer(self, answer):
        #Uses constant-time comparison to prevent timing attacks
        return check_password_hash(self.security_answer_hash, answer.lower())

