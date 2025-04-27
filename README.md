[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19343466&assignment_repo_type=AssignmentRepo)
# Flask restaurant listing

This codebase implements a basic restaurant listing web application using python and the flask framework. 

# Setup

To setup the basic website you will need to have the following installed:

- python3
- pip
- sqlite3

Pip is the package manager for Python.  You can install the remaining packages required for this task using pip. You will need to run the following:
To start you should create and activate a virtual environment:

- $ python -m venv env        # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
- $ source env/bin/activate   # use `env\Scripts\activate` on Windows
- $ pip install -r requirements.txt

You will also need sqlite installed for the database backend.

# Initialising the database

You should first initialise the database as follows:
- python initialise_db.py

This should create an sqlite database under the instance directory. You can view the contents of the database using the sqlite command line interface as follows:

sqlite3 instance/db.sqlite
> .schema  

CREATE TABLE restaurant (
	id INTEGER NOT NULL, 
	name VARCHAR(250) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE menu_item (
	name VARCHAR(80) NOT NULL, 
	id INTEGER NOT NULL, 
	description VARCHAR(250), 
	price VARCHAR(8), 
	course VARCHAR(250), 
	restaurant_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(restaurant_id) REFERENCES restaurant (id)
);
> select * from restaurant;
1|Urban Burger
2|Super Stir Fry
3|Panda Garden
4|Thyme for That Vegetarian Cuisine 
5|Tony's Bistro 
6|Andala's
7|Auntie Ann's Diner 
8|Cocina Y Amor 

You can see that the database comes prepopulated with some restaurants and some menu items. This is done in the initialise_db.py file.

# Run the website

You can run the website by typing:

- python run.py

You can now browse to the url http://localhost:8000/ to view the website.
