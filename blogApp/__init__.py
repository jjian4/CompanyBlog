import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from blogApp.posts.forms import NewPostForm

app = Flask(__name__)


#Secret key 
app.config['SECRET_KEY'] = 'mysecretkey'

#SQLite Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)


#Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
#Which view to go to when logging in
login_manager.login_view = "users.login"



#Navbar channel options - display departments names from NewPostForm in every template
@app.context_processor
def inject_departments():
	departments = NewPostForm.departments
	return dict(departments=departments)


@app.context_processor
def inject_current_user():
	return dict(current_user=current_user)



#Blueprint connections
from blogApp.core.views import core
app.register_blueprint(core)
from blogApp.users.views import users
app.register_blueprint(users)
from blogApp.posts.views import posts
app.register_blueprint(posts)

from blogApp.errors import error_pages
app.register_blueprint(error_pages)
