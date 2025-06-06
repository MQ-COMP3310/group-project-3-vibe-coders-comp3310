from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Restaurant, MenuItem 
from sqlalchemy import asc
from . import db
#added to import login 
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Restaurant, MenuItem

main = Blueprint('main', __name__)

#Show all restaurants
@main.route('/')
@main.route('/restaurant/')
def showRestaurants():
  restaurants = db.session.query(Restaurant).order_by(asc(Restaurant.name))
  return render_template('restaurants.html', restaurants = restaurants)

#Create a new restaurant
@main.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
  if request.method == 'POST':
      newRestaurant = Restaurant(name = request.form['name'])
      db.session.add(newRestaurant)
      flash('New Restaurant %s Successfully Created' % newRestaurant.name)
      db.session.commit()
      return redirect(url_for('main.showRestaurants'))
  else:
      return render_template('newRestaurant.html')

#Edit a restaurant
@main.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
  editedRestaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedRestaurant.name = request.form['name']
        flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
        return redirect(url_for('main.showRestaurants'))
  else:
    return render_template('editRestaurant.html', restaurant = editedRestaurant)


#Delete a restaurant
@main.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
  restaurantToDelete = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
    db.session.delete(restaurantToDelete)
    flash('%s Successfully Deleted' % restaurantToDelete.name)
    db.session.commit()
    return redirect(url_for('main.showRestaurants', restaurant_id = restaurant_id))
  else:
    return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)

#Show a restaurant menu
@main.route('/restaurant/<int:restaurant_id>/')
@main.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', items = items, restaurant = restaurant)
     


#Create a new menu item
@main.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
      db.session.add(newItem)
      db.session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
  else:
      return render_template('newmenuitem.html', restaurant_id = restaurant_id)

#Edit a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):

    editedItem = db.session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        db.session.add(editedItem)
        db.session.commit() 
        flash('Menu Item Successfully Edited')
        return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


#Delete a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    itemToDelete = db.session.query(MenuItem).filter_by(id = menu_id).one() 
    if request.method == 'POST':
        db.session.delete(itemToDelete)
        db.session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item = itemToDelete)
    
#Task 7added login logout and register routes

#login route with authentication checks
@main.route('/login', methods=['GET', 'POST'])
def login():
    #Checks if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.showRestaurants'))
        
    if request.method == 'POST':
        #should add rate limiting to prevent brute force attacks
        username = request.form['username']
        password = request.form['password']
        #parameterized query to prevent SQL injection
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            #session management with flask login
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.showRestaurants'))
        else:
            #generic error message to prevent username enumeration
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

#logout route
@main.route('/logout')
@login_required
def logout():
    #proper session termination
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.showRestaurants'))

#Registration route with input validation
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.showRestaurants'))
        
    if request.method == 'POST':
        #should add imput sanitization for email and password
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        #additional feature 1
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        
        #check for existing to prevent duplicates
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'danger')
            return redirect(url_for('main.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('main.register'))
        
        #additional feature 1
        user = User(username=username, email=email, security_question=security_question)
        #password hashing done in user model
        user.set_password(password)
        user.set_security_answer(security_answer)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

#task 9 additional feature 1
@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        
        if not user:
            #generic message to prevent username enumeration
            flash('Username not found', 'danger')
            return redirect(url_for('main.forgot_password'))

        #in real world implementation, an email would be sent
        #however here we redirect directly to simulate flow   
        return redirect(url_for('main.reset_password', username=user.username))
    
    return render_template('forgot_password.html')

#task 9 additional feature 1
@main.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    username = request.args.get('username') or request.form.get('username')
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('Invalid request', 'danger')
        return redirect(url_for('main.forgot_password'))
    
    #should add limit rate limiting here to prevent automation
    if request.method == 'POST':
        security_answer = request.form['security_answer']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        #verify security answer by comparing hash
        if not user.check_security_answer(security_answer):
            flash('Incorrect security answer', 'danger')
            return render_template('reset_password.html',
                                 username=user.username,
                                 security_question=user.security_question)
        
        #password confirmation check
        if new_password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('reset_password.html',
                                 username=user.username,
                                 security_question=user.security_question)
        
        #update password and hashed automatically
        user.set_password(new_password)
        db.session.commit()
        flash('Password reset successfully! Please login with your new password', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('reset_password.html',
                         username=user.username,
                         security_question=user.security_question)