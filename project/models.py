from . import db
#import werkzeug securtiy to  hash passwords
from werkzeug.security import generate_password_hash, check_password_hash

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    #added a user ID to link restaurant and user
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    restaurant = db.    relationship(Restaurant)

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
    
    #new user model
class User(db.Model):
    #user details
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    isAdmin = db.Column(db.Boolean, default=False)

    restaurant = db.relationship(Restaurant,backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % (self.username)
    #hashes password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    #check password against hash
    def check_password(self, password):
        return check_password_hash(self.password, password)

