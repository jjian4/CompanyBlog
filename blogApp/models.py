from blogApp import db, login_manager
#To generate password hash and check password
from werkzeug.security import generate_password_hash,check_password_hash
#For authentication
from flask_login import UserMixin
#To get current date/time for Post objects
from datetime import datetime


#Use login_manager to check authentication in templates
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#User object
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    position = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    #Connect Post objects to Users
    posts = db.relationship('Post', backref='author', lazy=True)

    #User initialization
    def __init__(self, email, username, position, password):
        self.email = email
        self.username = username
        self.position = position
        self.password_hash = generate_password_hash(password)

    #Will use to check if password provided at login matches registered password
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    #For printing out User (won't be used)
    def __repr__(self):
        return f"{self.username}: {self.position}"



#Post object
class Post(db.Model):
    # Connect to the User table
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    #Set User id as foreign key, Every Post must have a User so nullable=False
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)

    #Post initialization
    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id

    #For printing out Post (won't be used)
    def __repr__(self):
        return f"{self.id}, {self.date}, {self.title}: {self.text}"








