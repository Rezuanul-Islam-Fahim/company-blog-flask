from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    profile_img = db.Column(
        db.String(64),
        nullable=False,
        default='default_profile.jpg'
    )
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Username: {self.username}, Email: {self.email}'

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_img': self.profile_img
        }


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, desc, author_id):
        self.title = title
        self.desc = desc
        self.author_id = author_id

    def __repr__(self):
        return f'Title: {self.title}, datetime: {self.datetime}, desc: {self.desc}'
