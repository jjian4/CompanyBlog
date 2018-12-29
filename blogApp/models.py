from blogApp import db, login_manager
#To generate password hash and check password
from werkzeug.security import generate_password_hash,check_password_hash
#For authentication
from flask_login import UserMixin
#To get current date/time for Post objects
from datetime import datetime
#To save current_user.id as user_id in Reply
from flask_login import current_user


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

    #Connect Reply objects to Users
    replies = db.relationship('Reply', backref='replier', lazy=True)

    #User initialization
    def __init__(self, email, username, position, password):
        self.email = email
        self.username = username
        self.position = position
        self.password_hash = generate_password_hash(password)

    #Will use to check if password provided at login matches registered password
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    #For default printing out User (won't be used)
    def __repr__(self):
        return f"{self.username}: {self.position}"


#Post object
class Post(db.Model):

    __tablename__ = 'posts'

    # Connect to the User table
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    #Set User id as foreign key, Every Post must have a User so nullable=False
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    title = db.Column(db.String(128), nullable=False)
    department = db.Column(db.String(128))
    text = db.Column(db.Text, nullable=False)

    #Connect Reply objects to Posts
    replies = db.relationship('Reply', backref='parent_post', lazy=True)

    #Post initialization
    def __init__(self, title, department, text, user_id):
        self.title = title
        self.department = department
        self.text = text
        self.user_id =user_id

    #For default printing out Post (won't be used)
    def __repr__(self):
        return f"{self.id}, {self.date}, {self.title}: {self.text}"




#Replies to posts
class Reply(db.Model):

    # Connect to the Post table
    posts = db.relationship(Post)

    id = db.Column(db.Integer, primary_key=True)

    #Set Post id as foreign key, Every Reply must have a Post so nullable=False
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    #Set User id as foreign key, Every Reply must have a User so nullable=False
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    #Reply initialization
    def __init__(self, text, post_id):
        self.text = text
        self.post_id = post_id
        self.user_id = current_user.id

    #For default printing out Reply (won't be used)
    def __repr__(self):
        return f"{self.user_id}, {self.date}, to Post#{self.post_id}: {self.text}"




