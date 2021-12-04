from datetime import datetime
from flask_login import UserMixin
from myProject import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String , unique=True,index=True)
    email = db.Column(db.String , unique=True,index=True)
    password = db.Column(db.String)
    confirm_pass = db.Column(db.String)
    profile_image = db.Column(db.String,nullable=False,default='default_image.jpg')

    posts = db.relationship('Post',backref='user',lazy=True)

    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

class Post(db.Model,UserMixin):

    __tablename__ = 'posts'
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.Text,nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text= text
        self.user_id = user_id

    def __repr__(self):
        return f"Post Id: {self.id}"