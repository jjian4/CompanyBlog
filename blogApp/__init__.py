import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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


#Blueprint connections
from blogApp.core.views import core
app.register_blueprint(core)
from blogApp.errors import error_pages
app.register_blueprint(error_pages)
